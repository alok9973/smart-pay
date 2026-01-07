from datetime import datetime

walletdata = {
    "banks": {
        "BANK001": {
            "bank_id": "BANK001",
            "bank_name": "State Bank of India",
            "ifsc_code": "SBIN0000123"
        },
        "BANK002": {
            "bank_id": "BANK002",
            "bank_name": "HDFC Bank",
            "ifsc_code": "HDFC0000456"
        },
        "BANK003": {
            "bank_id": "BANK003",
            "bank_name": "ICICI Bank",
            "ifsc_code": "ICIC0000789"
        }
    },
    "users": {
        "U1001": {
            "name": "Alok",
            "phone": "7070554929",
            "otp": "123456",
            "is_authenticated": False,
            "wallet": {
                "wallet_id": "W1001",
                "balance": 524.00
            },
            "linked_banks": [
                {
                    "bank_id": "BANK001",
                    "account_number": "1234567890123",
                    "ifsc_code": "SBIN0000123",
                    "account_holder_name": "Alok Kumar",
                    "is_primary": True,
                    "linked_date": "2025-12-01T10:00:00"
                }
            ],
            "transactions": [
                {
                    "transaction_id": "TXN001",
                    "type": "CREDIT",
                    "amount": 500.00,
                    "from_user": "self",
                    "to_user": "U1001",
                    "description": "Initial wallet credit",
                    "timestamp": "2025-12-01T10:00:00",
                    "status": "SUCCESS"
                }
            ]
        },
        "U1002": {
            "name": "Drishti",
            "phone": "1234567890",
            "otp": "654321",
            "is_authenticated": False,
            "wallet": {
                "wallet_id": "W1002",
                "balance": 1024.50
            },
            "linked_banks": [
                {
                    "bank_id": "BANK002",
                    "account_number": "9876543210987",
                    "ifsc_code": "HDFC0000456",
                    "account_holder_name": "Drishti Singh",
                    "is_primary": True,
                    "linked_date": "2025-11-15T14:30:00"
                }
            ],
            "transactions": [
                {
                    "transaction_id": "TXN002",
                    "type": "CREDIT",
                    "amount": 1000.00,
                    "from_user": "self",
                    "to_user": "U1002",
                    "description": "Initial wallet credit",
                    "timestamp": "2025-11-15T14:30:00",
                    "status": "SUCCESS"
                },
                {
                    "transaction_id": "TXN003",
                    "type": "DEBIT",
                    "amount": 50.00,
                    "from_user": "U1002",
                    "to_user": "U1001",
                    "description": "Payment for services",
                    "timestamp": "2025-12-05T11:20:00",
                    "status": "SUCCESS"
                }
            ]
        },
        "U1003": {
            "name": "xyz",
            "phone": "7823456787",
            "otp": "111222",
            "is_authenticated": False,
            "wallet": {
                "wallet_id": "W1003",
                "balance": 250.75
            },
            "linked_banks": [],
            "transactions": [
                {
                    "transaction_id": "TXN004",
                    "type": "CREDIT",
                    "amount": 250.75,
                    "from_user": "self",
                    "to_user": "U1003",
                    "description": "Initial wallet credit",
                    "timestamp": "2025-12-10T09:15:00",
                    "status": "SUCCESS"
                }
            ]
        }
    },
    "bank_accounts": {
        "ACC001": {
            "account_id": "ACC001",
            "bank_id": "BANK001",
            "account_number": "1234567890123",
            "ifsc_code": "SBIN0000123",
            "account_holder_name": "Alok Kumar",
            "balance": 50000.00
        },
        "ACC002": {
            "account_id": "ACC002",
            "bank_id": "BANK002",
            "account_number": "9876543210987",
            "ifsc_code": "HDFC0000456",
            "account_holder_name": "Drishti Singh",
            "balance": 75000.00
        },
        "ACC003": {
            "account_id": "ACC003",
            "bank_id": "BANK003",
            "account_number": "5555666677778",
            "ifsc_code": "ICIC0000789",
            "account_holder_name": "Test User",
            "balance": 25000.00
        }
    }
}
