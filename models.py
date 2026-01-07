from pydantic import BaseModel

class AuthRequest(BaseModel):
    mobile_number: str

class OTPVerifyRequest(BaseModel):
    user_id: str
    otp: str

class WalletRequest(BaseModel):
    user_id: str
