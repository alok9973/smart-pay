from fastapi import FastAPI, HTTPException
from models import AuthRequest, OTPVerifyRequest, WalletRequest
from data import walletdata

app = FastAPI(title="SmartPay Agent API")

# --------------------------
# Utility
# --------------------------
def check_valid_mobile_number(mobile_number: str) -> bool:
    return mobile_number.isdigit() and len(mobile_number) == 10 and mobile_number[0] != "0"

# --------------------------
# AUTH: Step 1 – Mobile Number
# --------------------------
@app.post("/authenticate")
def authenticate_user(request: AuthRequest):
    if not check_valid_mobile_number(request.mobile_number):
        return {
            "success": False,
            "message": "Invalid mobile number"
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
