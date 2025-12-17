from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.transfer_service import transfer_funds

router = APIRouter()

class TransferRequest(BaseModel):
    source_account_id: str
    destination_account_id: str
    amount: float
    currency: str
    description: str | None = None

@router.post("/transfers")
def transfer_endpoint(req: TransferRequest):
    try:
        transaction_id = transfer_funds(
            req.source_account_id,
            req.destination_account_id,
            req.amount,
            req.currency,
            req.description
        )
        return {"transaction_id": str(transaction_id)}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
