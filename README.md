# SmartPay - Digital Wallet Payment API

A comprehensive FastAPI-based digital wallet and payment management system with support for user authentication, wallet management, bank account linking, and peer-to-peer transactions.

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alok9973/smart-pay.git
   cd smart-pay
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start FastAPI Server**
   ```bash
   uvicorn main:app --reload
   ```
   Verify locally: http://127.0.0.1:8000/docs

5. **Expose API using ngrok**
   ```bash
   ngrok http 8000
   ```
   You will receive a public URL like: `https://xxxx.ngrok-free.app`

## Features

**User Authentication** - Mobile OTP verification
**Wallet Management** - Balance checking and transfers  
**Bank Integration** - Link banks, add money from bank accounts
**Transaction History** - View all transactions or filter by phone
**Money Transfer** - Transfer to any registered user
**Edge Case Handling** - Complete validation and error handling

## API Endpoints

### Authentication
- `POST /authenticate` - Authenticate with mobile number
- `POST /verify-otp` - Verify OTP

### Wallet Operations
- `POST /wallet/balance` - Check wallet balance
- `POST /wallet/transaction-history` - Get transaction history (optionally filter by mobile number)
- `POST /wallet/transfer-money` - Transfer money to another registered user
- `POST /wallet/add-money-from-bank` - Add money from linked bank account

### Bank Management
- `POST /bank/link-account` - Link a new bank account (checks if not already linked, then links it)
- `POST /bank/get-linked-banks` - Get all linked bank accounts

### System
- `GET /health` - API health check

## Dummy Data Included

### Users
- **U1001** - Alok (Phone: 7070554929, Balance: ₹524.00)
- **U1002** - Drishti (Phone: 1234567890, Balance: ₹1024.50)  
- **U1003** - xyz (Phone: 7823456787, Balance: ₹250.75)

### Banks
- **BANK001** - State Bank of India (IFSC: SBIN0000123)
- **BANK002** - HDFC Bank (IFSC: HDFC0000456)
- **BANK003** - ICICI Bank (IFSC: ICIC0000789)

### Bank Accounts
- **ACC001** - SBI Account: ₹50,000 (Linked to U1001)
- **ACC002** - HDFC Account: ₹75,000 (Linked to U1002)
- **ACC003** - ICICI Account: ₹25,000 (Available for linking)

### Sample Transactions
- U1001 & U1002 have pre-loaded transaction histories

## Edge Cases & Validation Implemented

### Mobile Number Validation
- Must be exactly 10 digits
- Cannot start with 0
- Invalid format error handling

### Amount Validation
- Amount must be greater than 0
- Maximum transfer limit: ₹50,000
- Maximum bank deposit limit: ₹100,000
- Insufficient balance detection

### Bank Management
- Bank ID validation
- IFSC code matching with bank
- Duplicate bank account linking prevention
- Bank linking verification before transfers
- Bank account balance sufficiency check

### Transaction Management
- User existence verification
- Authentication state checking (all protected endpoints)
- Self-transfer prevention
- Transaction history filtering by mobile number
- Invalid recipient handling
- Both sender and recipient transaction recording

### Other Edge Cases
- User not found error handling
- OTP verification failure handling
- Duplicate transactions prevention
- Consistent transaction IDs (UUID-based)
- Timestamp recording for all transactions

## Testing Guide

### Using Swagger UI (Recommended)
1. Start the server: `uvicorn main:app --reload`
2. Open: http://127.0.0.1:8000/docs
3. Try out endpoints interactively

### Using cURL

```bash
# 1. Authenticate
curl -X POST "http://127.0.0.1:8000/authenticate" \
  -H "Content-Type: application/json" \
  -d '{"mobile_number": "7070554929"}'

# 2. Verify OTP
curl -X POST "http://127.0.0.1:8000/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001", "otp": "123456"}'

# 3. Check Balance
curl -X POST "http://127.0.0.1:8000/wallet/balance" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001"}'

# 4. Get Transaction History
curl -X POST "http://127.0.0.1:8000/wallet/transaction-history" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001"}'

# 5. Get Transaction History for Specific User
curl -X POST "http://127.0.0.1:8000/wallet/transaction-history" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001", "mobile_number": "1234567890"}'

# 6. Link Bank Account (for U1003 which has no linked banks)
curl -X POST "http://127.0.0.1:8000/bank/link-account" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1003", "bank_id": "BANK003", "account_number": "5555666677778", "ifsc_code": "ICIC0000789", "account_holder_name": "Test User"}'

# 7. Get Linked Banks
curl -X POST "http://127.0.0.1:8000/bank/get-linked-banks" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001"}'

# 8. Add Money from Bank
curl -X POST "http://127.0.0.1:8000/wallet/add-money-from-bank" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001", "bank_id": "BANK001", "amount": 1000}'

# 9. Transfer Money to Another User
curl -X POST "http://127.0.0.1:8000/wallet/transfer-money" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "U1001", "recipient_mobile_number": "1234567890", "amount": 100, "description": "Payment for services"}'
```

## Project Structure

```
smart-pay/
├── main.py              # FastAPI application with all endpoints
├── models.py            # Pydantic request/response data models
├── data.py              # Dummy data (users, banks, transactions, accounts)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## File Details

### main.py
- Authentication endpoints
- Wallet operations (balance, transactions, transfers)
- Bank management (linking, adding money)
- Full error handling and validation

### models.py
- AuthRequest
- OTPVerifyRequest
- WalletRequest
- TransactionHistoryRequest
- LinkBankRequest
- AddMoneyFromBankRequest
- TransferMoneyRequest

### data.py
- User data with wallets and transaction history
- Bank information
- Bank account data
- Transaction history for each user

## Technologies Used

- **FastAPI** - Modern async Python web framework
- **Pydantic** - Data validation using Python type annotations
- **Python 3.8+** - Programming language
- **ngrok** - Secure tunneling for public API access
- **Uvicorn** - ASGI server

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true/false,
  "message": "Description of result",
  "data": {}
}
```

## Error Handling

Comprehensive error responses with meaningful messages:

- Invalid input validation
- User existence checks
- Authentication verification
- Balance sufficiency checks
- Bank linking verification
- IFSC code validation
- Duplicate prevention
- Limit enforcement

## Testing Scenarios

### Scenario 1: New User Linking Bank and Adding Money
1. User U1003 (xyz) has no linked banks
2. Link BANK003 using `/bank/link-account`
3. Add ₹5000 from BANK003 using `/wallet/add-money-from-bank`
4. Check balance increased

### Scenario 2: Transfer Between Users
1. User U1001 transfers ₹100 to U1002
2. Check transaction history for both users
3. Verify balances are updated correctly

### Scenario 3: Filter Transactions by Phone Number
1. Get all transactions for U1001
2. Filter transactions involving U1002 (1234567890)
3. Verify only relevant transactions are shown

### Scenario 4: Edge Cases
- Try to transfer to own account (should fail)
- Try to add ₹0 (should fail)
- Try to add more than bank balance (should fail)
- Try to link already linked bank (should fail)
- Try to use wrong IFSC code (should fail)

