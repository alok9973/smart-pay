from fastapi import FastAPI, HTTPException
from models import (
    AuthRequest, OTPVerifyRequest, WalletRequest, 
    TransactionHistoryRequest, LinkBankRequest, 
    AddMoneyFromBankRequest, TransferMoneyRequest
)
from data import walletdata
from datetime import datetime
import uuid

app = FastAPI(title="SmartPay Agent API")

# --------------------------
# Utility Functions
# --------------------------
def check_valid_mobile_number(mobile_number: str) -> bool:
    return mobile_number.isdigit() and len(mobile_number) == 10 and mobile_number[0] != "0"

def generate_transaction_id() -> str:
    return f"TXN{uuid.uuid4().hex[:12].upper()}"

def find_user_by_phone(phone: str):
    """Find user by phone number"""
    for user_id, user in walletdata["users"].items():
        if user["phone"] == phone:
            return user_id, user
    return None, None

def get_current_timestamp() -> str:
    return datetime.now().isoformat()

# --------------------------
# AUTH: Step 1 – Mobile Number
# --------------------------
@app.post("/authenticate")
def authenticate_user(request: AuthRequest):
    if not check_valid_mobile_number(request.mobile_number):
        return {
            "success": False,
            "message": "Invalid mobile number. Must be 10 digits and not start with 0"
        }

    for user_id, user in walletdata["users"].items():
        if user["phone"] == request.mobile_number:
            return {
                "success": True,
                "message": "OTP sent to registered mobile number",
                "user_id": user_id
            }

    return {
        "success": False,
        "message": "User not found. Please register."
    }

# --------------------------
# AUTH: Step 2 – OTP Verify
# --------------------------
@app.post("/verify-otp")
def verify_otp(request: OTPVerifyRequest):
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.otp != user["otp"]:
        return {
            "success": False,
            "message": "Invalid OTP"
        }

    user["is_authenticated"] = True

    return {
        "success": True,
        "message": "Authentication successful! You’re now securely connected to SmartPay."
    }

# --------------------------
# WALLET: Check Balance (Protected)
# --------------------------
@app.post("/wallet/balance")
def check_balance(request: WalletRequest):
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    return {
        "success": True,
        "wallet_id": user["wallet"]["wallet_id"],
        "balance": user["wallet"]["balance"]
    }

# --------------------------
# TRANSACTION HISTORY: Get transactions for a user
# --------------------------
@app.post("/transaction-history")
def get_transaction_history(request: TransactionHistoryRequest):
    """Get all transactions for authenticated user"""
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    # Get transactions directly from user data
    transactions = user.get("transactions", [])

    return transactions


# --------------------------
# BANK: Link Bank Account
# --------------------------
@app.post("/bank/link-account")
def link_bank_account(request: LinkBankRequest):
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    # Validate bank exists
    bank = walletdata["banks"].get(request.bank_id)
    if not bank:
        return {
            "success": False,
            "message": f"Bank with ID {request.bank_id} not found"
        }

    # Validate IFSC code matches bank
    if bank["ifsc_code"] != request.ifsc_code:
        return {
            "success": False,
            "message": f"IFSC code does not match bank. Expected: {bank['ifsc_code']}"
        }

    # Check if bank is already linked
    linked_banks = user.get("linked_banks", [])
    for linked_bank in linked_banks:
        if linked_bank["bank_id"] == request.bank_id and linked_bank["account_number"] == request.account_number:
            return {
                "success": False,
                "message": "This bank account is already linked to your wallet"
            }

    # Link the bank
    new_bank_link = {
        "bank_id": request.bank_id,
        "account_number": request.account_number,
        "ifsc_code": request.ifsc_code,
        "account_holder_name": request.account_holder_name,
        "is_primary": len(linked_banks) == 0,  # First bank is primary
        "linked_date": get_current_timestamp()
    }

    if "linked_banks" not in user:
        user["linked_banks"] = []
    
    user["linked_banks"].append(new_bank_link)

    return {
        "success": True,
        "message": f"Bank account {request.account_number} linked successfully",
        "bank_name": bank["bank_name"],
        "is_primary": new_bank_link["is_primary"]
    }

# --------------------------
# BANK: Add Money from Bank Account
# --------------------------
@app.post("/wallet/add-money-from-bank")
def add_money_from_bank(request: AddMoneyFromBankRequest):
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    # Validate amount
    if request.amount <= 0:
        return {
            "success": False,
            "message": "Amount must be greater than 0"
        }

    if request.amount > 100000:
        return {
            "success": False,
            "message": "Amount exceeds maximum transaction limit of 100,000"
        }

    # Check if bank is linked
    linked_banks = user.get("linked_banks", [])
    bank_link = None
    for linked_bank in linked_banks:
        if linked_bank["bank_id"] == request.bank_id:
            bank_link = linked_bank
            break

    if not bank_link:
        return {
            "success": False,
            "message": f"Bank {request.bank_id} is not linked with your account. Please link it first."
        }

    # Validate bank account has sufficient balance
    bank_account = None
    for acc in walletdata["bank_accounts"].values():
        if acc["bank_id"] == request.bank_id and acc["account_number"] == bank_link["account_number"]:
            bank_account = acc
            break

    if not bank_account:
        return {
            "success": False,
            "message": "Bank account not found in system"
        }

    if bank_account["balance"] < request.amount:
        return {
            "success": False,
            "message": f"Insufficient balance in bank account. Available: {bank_account['balance']}"
        }

    # Process transaction
    transaction_id = generate_transaction_id()
    
    # Deduct from bank account
    bank_account["balance"] -= request.amount
    
    # Add to wallet
    user["wallet"]["balance"] += request.amount

    # Record transaction
    if "transactions" not in user:
        user["transactions"] = []

    transaction = {
        "transaction_id": transaction_id,
        "type": "CREDIT",
        "amount": request.amount,
        "from_user": "BANK",
        "to_user": request.user_id,
        "description": f"Money added from {walletdata['banks'][request.bank_id]['bank_name']}",
        "timestamp": get_current_timestamp(),
        "status": "SUCCESS"
    }

    user["transactions"].append(transaction)

    return {
        "success": True,
        "message": f"Successfully added ₹{request.amount} to your wallet",
        "transaction_id": transaction_id,
        "new_balance": user["wallet"]["balance"],
        "timestamp": transaction["timestamp"]
    }

# --------------------------
# WALLET: Transfer Money to Another User
# --------------------------
@app.post("/wallet/transfer-money")
def transfer_money(request: TransferMoneyRequest):
    sender = walletdata["users"].get(request.user_id)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender user not found")

    if not sender["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    # Validate amount
    if request.amount <= 0:
        return {
            "success": False,
            "message": "Amount must be greater than 0"
        }

    if request.amount > 50000:
        return {
            "success": False,
            "message": "Amount exceeds maximum transfer limit of 50,000"
        }

    # Validate recipient mobile number
    if not check_valid_mobile_number(request.recipient_mobile_number):
        return {
            "success": False,
            "message": "Invalid recipient mobile number format"
        }

    # Find recipient
    recipient_user_id, recipient = find_user_by_phone(request.recipient_mobile_number)

    if not recipient_user_id or not recipient:
        return {
            "success": False,
            "message": f"No user found with mobile number {request.recipient_mobile_number}"
        }

    # Prevent self-transfer
    if request.user_id == recipient_user_id:
        return {
            "success": False,
            "message": "Cannot transfer money to your own account"
        }

    # Check sender balance
    if sender["wallet"]["balance"] < request.amount:
        return {
            "success": False,
            "message": f"Insufficient balance. Available: ₹{sender['wallet']['balance']}"
        }

    # Process transaction
    transaction_id = generate_transaction_id()
    timestamp = get_current_timestamp()

    # Deduct from sender
    sender["wallet"]["balance"] -= request.amount

    # Add to recipient
    recipient["wallet"]["balance"] += request.amount

    # Record transaction in sender's history
    if "transactions" not in sender:
        sender["transactions"] = []

    sender_transaction = {
        "transaction_id": transaction_id,
        "type": "DEBIT",
        "amount": request.amount,
        "from_user": request.user_id,
        "to_user": recipient_user_id,
        "description": request.description,
        "recipient_name": recipient["name"],
        "recipient_phone": recipient["phone"],
        "timestamp": timestamp,
        "status": "SUCCESS"
    }

    sender["transactions"].append(sender_transaction)

    # Record transaction in recipient's history
    if "transactions" not in recipient:
        recipient["transactions"] = []

    recipient_transaction = {
        "transaction_id": transaction_id,
        "type": "CREDIT",
        "amount": request.amount,
        "from_user": request.user_id,
        "to_user": recipient_user_id,
        "description": request.description,
        "sender_name": sender["name"],
        "sender_phone": sender["phone"],
        "timestamp": timestamp,
        "status": "SUCCESS"
    }

    recipient["transactions"].append(recipient_transaction)

    return {
        "success": True,
        "message": f"Successfully transferred ₹{request.amount} to {recipient['name']}",
        "transaction_id": transaction_id,
        "recipient_name": recipient["name"],
        "recipient_phone": recipient["phone"],
        "amount_transferred": request.amount,
        "sender_new_balance": sender["wallet"]["balance"],
        "timestamp": timestamp
    }

# --------------------------
# BANK: Get Linked Banks
# --------------------------
@app.post("/bank/get-linked-banks")
def get_linked_banks(request: WalletRequest):
    user = walletdata["users"].get(request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user["is_authenticated"]:
        return {
            "success": False,
            "message": "Please authenticate first"
        }

    linked_banks = user.get("linked_banks", [])

    if not linked_banks:
        return {
            "success": True,
            "message": "No banks linked",
            "linked_banks": [],
            "count": 0
        }

    # Enrich with bank details
    enriched_banks = []
    for linked_bank in linked_banks:
        bank = walletdata["banks"].get(linked_bank["bank_id"])
        enriched_banks.append({
            "bank_id": linked_bank["bank_id"],
            "bank_name": bank["bank_name"] if bank else "Unknown",
            "account_number": linked_bank["account_number"],
            "ifsc_code": linked_bank["ifsc_code"],
            "account_holder_name": linked_bank["account_holder_name"],
            "is_primary": linked_bank["is_primary"],
            "linked_date": linked_bank["linked_date"]
        })

    return {
        "success": True,
        "linked_banks": enriched_banks,
        "count": len(enriched_banks)
    }

# --------------------------
# Health Check
# --------------------------
@app.get("/health")
def health_check():
    return {"status": "SmartPay API is running", "timestamp": get_current_timestamp()}
