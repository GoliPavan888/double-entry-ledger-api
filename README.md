# Double Entry Ledger API

A production-grade **double-entry bookkeeping system** built with **FastAPI** and **PostgreSQL**, designed to safely handle deposits, withdrawals, and transfers with full transactional integrity.

This project demonstrates how real financial systems track balances using an **immutable ledger**, rather than storing balances directly.

---

## 🚀 Features

- Double-entry accounting model
- Immutable ledger entries
- ACID-safe transactions
- Concurrency-safe withdrawals and transfers
- Ledger-based balance calculation
- Dockerized setup
- Clean layered architecture (Controller → Service → Repository)

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI**
- **PostgreSQL**
- **psycopg2**
- **Docker & Docker Compose**

---

## 📐 Architecture Overview

Client
↓
FastAPI Controllers
↓
Service Layer (business logic)
↓
Repository Layer (DB access)
↓
PostgreSQL
├── accounts
├── transactions
└── ledger_entries


- Controllers handle HTTP and validation
- Services enforce business rules
- Repositories perform database operations
- PostgreSQL guarantees transactional safety

---

## 🗄️ Database Design

### Tables

#### `accounts`
- Represents a financial account
- One row per account
- Used for locking during withdrawals and transfers

#### `transactions`
- High-level financial events (deposit, withdrawal, transfer)
- Used for audit and traceability

#### `ledger_entries`
- Immutable records of all money movements
- Source of truth for balances
- Credits are positive, debits are negative

📌 **Balances are never stored** — they are always calculated from the ledger.

---

## 🔐 Why Balances Are Not Stored

Storing balances introduces:
- Data inconsistency
- Race conditions
- Reconciliation complexity

Instead, this system:
- Calculates balances using `SUM(ledger_entries.amount)`
- Guarantees correctness through immutability
- Enables full auditing and replayability

This is how real banking and accounting systems work.

---

## 🔒 Concurrency & ACID Guarantees

### Withdrawals
- Lock the account row using `SELECT ... FOR UPDATE`
- Prevent concurrent overdrafts
- Reject insufficient funds with HTTP `422`

### Transfers
- Lock **both accounts**
- Lock order is deterministic to prevent deadlocks
- Write exactly **two ledger entries**
  - Debit source
  - Credit destination
- Transaction rolls back completely on failure

---

## 📡 API Endpoints

### Accounts
- `POST /accounts` — Create account
- `GET /accounts/{id}` — Get account with balance
- `GET /accounts/{id}/ledger` — Get ledger entries

### Money Movement
- `POST /deposits` — Deposit funds
- `POST /withdrawals` — Withdraw funds (with balance check)
- `POST /transfers` — Transfer funds between accounts

---

## 📥 Example API Flows

### Create Account
POST /accounts
{
  "user_id": "11111111-1111-1111-1111-111111111111",
  "account_type": "checking",
  "currency": "USD"
}

### Deposit
POST /deposits
{
  "account_id": "ACCOUNT_ID",
  "amount": 100,
  "currency": "USD"
}

### Withdrawal (Insufficient Funds)
POST /withdrawals
{
  "account_id": "ACCOUNT_ID",
  "amount": 100000,
  "currency": "USD"
}
## Response:
422 Unprocessable Entity
{
  "detail": "Insufficient funds"
}

### Transfer
POST /transfers
{
  "source_account_id": "ACCOUNT_A",
  "destination_account_id": "ACCOUNT_B",
  "amount": 25,
  "currency": "USD"
}

### 🐳 Running the Project

## 1️⃣ Clone Repository

git clone <repo-url>
cd double-entry-ledger-api

## 2️⃣ Configure Environment
cp .env.example .env

## 3️⃣ Start with Docker
docker compose up --build

## 4️⃣ Open Swagger UI
http://localhost:8000/docs



📂 Project Structure

src/
├── controllers/
├── services/
├── repositories/
├── db/
│   └── schema.sql
└── main.py

docs/
├── database-erd.png
├── architecture-diagram.png
└── postman_collection.json

📌 See `docs/architecture-diagram.md` for the full system architecture.
📌 See `docs/erd.png` for the database schema.
