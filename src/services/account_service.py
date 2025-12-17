from src.repositories.account_repository import create_account, get_account
from src.repositories.ledger_repository import calculate_balance

def create_new_account(user_id, account_type, currency):
    return create_account(user_id, account_type, currency)

def get_account_with_balance(account_id):
    account = get_account(account_id)
    if not account:
        return None
    balance = calculate_balance(account_id)
    account["balance"] = balance
    return account
