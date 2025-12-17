import uuid
from src.db.database import get_connection

def create_account(user_id, account_type, currency):
    account_id = uuid.uuid4()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO accounts (id, user_id, account_type, currency, status)
                VALUES (%s, %s, %s, %s, 'active')
            """, (
                str(account_id),
                str(user_id),
                account_type,
                currency
            ))

    return account_id


def get_account(account_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM accounts
                WHERE id = %s
            """, (str(account_id),))
            return cur.fetchone()
