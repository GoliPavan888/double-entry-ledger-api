from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.account_service import (
    create_new_account,
    get_account_with_balance
)

router = APIRouter()   # ← REQUIRED

class AccountCreateRequest(BaseModel):
    user_id: str
    account_type: str
    currency: str

@router.post("/accounts")
def create_account_endpoint(req: AccountCreateRequest):
    account_id = create_new_account(
        req.user_id,
        req.account_type,
        req.currency
    )
    return {"account_id": account_id}

@router.get("/accounts/{account_id}")
def get_account_endpoint(account_id: str):
    account = get_account_with_balance(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
