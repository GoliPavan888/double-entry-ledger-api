import uuid
from src.db.database import get_connection

def create_deposit(account_id, amount, currency, description=None):
    transaction_id = uuid.uuid4()
    ledger_entry_id = uuid.uuid4()

    with get_connection() as conn:
        with conn.cursor() as cur:
            # Create transaction
            cur.execute("""
                INSERT INTO transactions (
                    id, type, destination_account_id,
                    amount, currency, status, description
                )
                VALUES (%s, 'deposit', %s, %s, %s, 'completed', %s)
            """, (
                str(transaction_id),
                str(account_id),
                amount,
                currency,
                description
            ))

            # Create ledger entry (CREDIT)
            cur.execute("""
                INSERT INTO ledger_entries (
                    id, account_id, transaction_id,
                    entry_type, amount
                )
                VALUES (%s, %s, %s, 'credit', %s)
            """, (
                str(ledger_entry_id),
                str(account_id),
                str(transaction_id),
                amount
            ))

    return transaction_id
