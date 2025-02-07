from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class TransactionDTO:
    id: UUID
    walletId: UUID
    txn_id: str
    from_wallet: str
    to_wallet: str
    amount: float
    transactionDate: datetime