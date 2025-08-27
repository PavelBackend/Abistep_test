from decimal import Decimal
from pydantic import BaseModel

class TransferRequest(BaseModel):
    from_user_id: int
    to_user_id: int
    amount: Decimal

class TransferResponse(BaseModel):
    sender_id: int
    receiver_id: int
    amount: Decimal
    detail: str