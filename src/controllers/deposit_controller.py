from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, condecimal
from src.services.deposit_service import deposit_to_account

router = APIRouter()

class DepositRequest(BaseModel):
    account_id: str
    amount: condecimal(gt=0)
    currency: str
    description: str | None = None

@router.post("/deposits")
def deposit_endpoint(req: DepositRequest):
    try:
        transaction_id = deposit_to_account(
            req.account_id,
            req.amount,
            req.currency,
            req.description
        )
        return {"transaction_id": transaction_id}
    except Exception:
        raise HTTPException(status_code=500, detail="Deposit failed")
