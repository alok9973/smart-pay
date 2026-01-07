from pydantic import BaseModel
from typing import Optional

class AuthRequest(BaseModel):
    mobile_number: str

class OTPVerifyRequest(BaseModel):
    user_id: str
    otp: str

class WalletRequest(BaseModel):
    user_id: str

class TransactionHistoryRequest(BaseModel):
    user_id: str
    mobile_number: Optional[str] = None

class LinkBankRequest(BaseModel):
    user_id: str
    bank_id: str
    account_number: str
    ifsc_code: str
    account_holder_name: str

class AddMoneyFromBankRequest(BaseModel):
    user_id: str
    bank_id: str
    amount: float

class TransferMoneyRequest(BaseModel):
    user_id: str
    recipient_mobile_number: str
    amount: float
    description: Optional[str] = "Transfer"

class GetTransactionHistoryResponse(BaseModel):
    success: bool
    user_id: str
    mobile_number: str
    transactions: list
    total_balance: float
