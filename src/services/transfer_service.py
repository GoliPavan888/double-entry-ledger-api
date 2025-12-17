from src.repositories.transfer_repository import create_transfer

def transfer_funds(source_account_id, destination_account_id, amount, currency, description=None):
    return create_transfer(
        source_account_id,
        destination_account_id,
        amount,
        currency,
        description
    )
