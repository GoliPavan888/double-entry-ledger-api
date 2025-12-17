## System Architecture Diagram

```mermaid
flowchart TB
    Client[Client / API Consumer]

    subgraph API["FastAPI Application"]
        Controllers[Controllers]
        Services[Service Layer]
        Repositories[Repository Layer]
    end

    subgraph DB["PostgreSQL Database"]
        Accounts[(accounts)]
        Transactions[(transactions)]
        Ledger[(ledger_entries)]
    end

    Client --> Controllers
    Controllers --> Services
    Services --> Repositories
    Repositories --> Accounts
    Repositories --> Transactions
    Repositories --> Ledger
