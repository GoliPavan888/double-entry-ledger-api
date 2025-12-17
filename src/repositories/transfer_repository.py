import uuid
from src.db.database import get_connection

def create_transfer(source_account_id, destination_account_id, amount, currency, description=None):
    transaction_id = uuid.uuid4()
    debit_entry_id = uuid.uuid4()
    credit_entry_id = uuid.uuid4()

    # Prevent deadlocks by locking in deterministic order
    first_lock, second_lock = sorted([
        str(source_account_id),
        str(destination_account_id)
    ])

    with get_connection() as conn:
        with conn.cursor() as cur:

            # 🔒 Lock both accounts
            cur.execute(
                "SELECT id FROM accounts WHERE id = %s FOR UPDATE",
                (first_lock,)
            )
            cur.execute(
                "SELECT id FROM accounts WHERE id = %s FOR UPDATE",
                (second_lock,)
            )

            # 🔍 Check source balance
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS balance
                FROM ledger_entries
                WHERE account_id = %s
            """, (str(source_account_id),))

            balance = cur.fetchone()["balance"]
            if balance < amount:
                raise ValueError("Insufficient funds")

            # 🧾 Create transaction
            cur.execute("""
                INSERT INTO transactions (
                    id, type, source_account_id, destination_account_id,
                    amount, currency, status, description
                )
                VALUES (%s, 'transfer', %s, %s, %s, %s, 'completed', %s)
            """, (
                str(transaction_id),
                str(source_account_id),
                str(destination_account_id),
                amount,
                currency,
                description
            ))

            # 📒 Debit source
            cur.execute("""
                INSERT INTO ledger_entries (
                    id, account_id, transaction_id,
                    entry_type, amount
                )
                VALUES (%s, %s, %s, 'debit', %s)
            """, (
                str(debit_entry_id),
                str(source_account_id),
                str(transaction_id),
                -amount
            ))

            # 📒 Credit destination
            cur.execute("""
                INSERT INTO ledger_entries (
                    id, account_id, transaction_id,
                    entry_type, amount
                )
                VALUES (%s, %s, %s, 'credit', %s)
            """, (
                str(credit_entry_id),
                str(destination_account_id),
                str(transaction_id),
                amount
            ))

    return transaction_id
