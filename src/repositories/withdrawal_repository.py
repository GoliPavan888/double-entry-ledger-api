import uuid
from src.db.database import get_connection

def create_withdrawal(account_id, amount, currency, description=None):
    transaction_id = uuid.uuid4()
    ledger_entry_id = uuid.uuid4()

    with get_connection() as conn:
        with conn.cursor() as cur:

            # 🔒 1. Lock the account row (prevents concurrent withdrawals)
            cur.execute("""
                SELECT id
                FROM accounts
                WHERE id = %s
                FOR UPDATE
            """, (str(account_id),))

            # 🔍 2. Calculate balance (no FOR UPDATE here)
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS balance
                FROM ledger_entries
                WHERE account_id = %s
            """, (str(account_id),))

            current_balance = cur.fetchone()["balance"]

            if current_balance < amount:
                raise ValueError("Insufficient funds")

            # 🧾 3. Create transaction
            cur.execute("""
                INSERT INTO transactions (
                    id, type, source_account_id,
                    amount, currency, status, description
                )
                VALUES (%s, 'withdrawal', %s, %s, %s, 'completed', %s)
            """, (
                str(transaction_id),
                str(account_id),
                amount,
                currency,
                description
            ))

            # 📒 4. Create debit ledger entry (negative amount)
            cur.execute("""
                INSERT INTO ledger_entries (
                    id, account_id, transaction_id,
                    entry_type, amount
                )
                VALUES (%s, %s, %s, 'debit', %s)
            """, (
                str(ledger_entry_id),
                str(account_id),
                str(transaction_id),
                -amount
            ))

    return transaction_id
