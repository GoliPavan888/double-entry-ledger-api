from src.repositories.ledger_repository import get_ledger_entries

def fetch_account_ledger(account_id):
    return get_ledger_entries(account_id)
