from src.repositories.withdrawal_repository import create_withdrawal

def withdraw_from_account(account_id, amount, currency, description=None):
    return create_withdrawal(account_id, amount, currency, description)
