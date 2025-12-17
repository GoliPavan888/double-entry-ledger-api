from src.db.database import get_connection

def calculate_balance(account_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS balance
                FROM ledger_entries
                WHERE account_id = %s
            """, (str(account_id),))
            return cur.fetchone()["balance"]


def get_ledger_entries(account_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    transaction_id,
                    entry_type,
                    amount,
                    created_at
                FROM ledger_entries
                WHERE account_id = %s
                ORDER BY created_at ASC
            """, (str(account_id),))
            return cur.fetchall()
