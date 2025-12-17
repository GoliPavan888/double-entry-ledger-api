from fastapi import APIRouter
from src.services.ledger_service import fetch_account_ledger

router = APIRouter()

@router.get("/accounts/{account_id}/ledger")
def get_account_ledger(account_id: str):
    return fetch_account_ledger(account_id)
