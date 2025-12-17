-- =========================
-- ACCOUNTS
-- =========================
CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    account_type TEXT NOT NULL,
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'frozen')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =========================
-- TRANSACTIONS
-- =========================
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('deposit', 'withdrawal', 'transfer')),
    source_account_id UUID NULL REFERENCES accounts(id),
    destination_account_id UUID NULL REFERENCES accounts(id),
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =========================
-- LEDGER ENTRIES (IMMUTABLE)
-- =========================
CREATE TABLE IF NOT EXISTS ledger_entries (
    id UUID PRIMARY KEY,
    account_id UUID NOT NULL REFERENCES accounts(id),
    transaction_id UUID NOT NULL REFERENCES transactions(id),
    entry_type TEXT NOT NULL CHECK (entry_type IN ('debit', 'credit')),
    amount NUMERIC(18,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =========================
-- INDEXES
-- =========================
CREATE INDEX IF NOT EXISTS idx_ledger_account_id
    ON ledger_entries(account_id);

CREATE INDEX IF NOT EXISTS idx_ledger_transaction_id
    ON ledger_entries(transaction_id);
