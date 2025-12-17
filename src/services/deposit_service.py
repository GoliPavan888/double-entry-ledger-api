from src.repositories.deposit_repository import create_deposit

def deposit_to_account(account_id, amount, currency, description=None):
    return create_deposit(account_id, amount, currency, description)
