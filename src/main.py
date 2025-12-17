from fastapi import FastAPI
from src.controllers.account_controller import router as account_router
from src.controllers.ledger_controller import router as ledger_router
from src.controllers.deposit_controller import router as deposit_router
from src.controllers.withdrawal_controller import router as withdrawal_router
from src.controllers.transfer_controller import router as transfer_router

app = FastAPI(title="Double Entry Ledger API")

app.include_router(account_router)
app.include_router(ledger_router)
app.include_router(deposit_router)
app.include_router(withdrawal_router)
app.include_router(transfer_router)

@app.get("/health")
def health():
    return {"status": "ok"}
