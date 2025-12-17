from fastapi import FastAPI
from src.controllers.account_controller import router as account_router

app = FastAPI(title="Double Entry Ledger API")

app.include_router(account_router)  # ← THIS LINE WAS THE ISSUE

@app.get("/health")
def health():
    return {"status": "ok"}
