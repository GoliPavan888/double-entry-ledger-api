from fastapi import FastAPI

app = FastAPI(title="Double Entry Ledger API")

@app.get("/health")
def health_check():
    return {"status": "ok"}