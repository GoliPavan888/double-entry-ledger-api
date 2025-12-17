from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, condecimal
from src.services.withdrawal_service import withdraw_from_account

router = APIRouter()

class WithdrawalRequest(BaseModel):
    account_id: str
    amount: condecimal(gt=0)
    currency: str
    description: str | None = None

@router.post("/withdrawals")
def withdrawal_endpoint(req: WithdrawalRequest):
    try:
        transaction_id = withdraw_from_account(
            req.account_id,
            req.amount,
            req.currency,
            req.description
        )
        return {"transaction_id": transaction_id}
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="Insufficient funds"
        )
