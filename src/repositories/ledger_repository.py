from src.db.database import get_connection

def calculate_balance(account_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS balance
                FROM ledger_entries
                WHERE account_id = %s
            """, (account_id,))
            return cur.fetchone()["balance"]
