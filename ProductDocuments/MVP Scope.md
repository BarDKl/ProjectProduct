# MVP Scope

# MoSCoW Scope — Safe-to-Spend Engine PoC

**Sprint Goal:** Ship a deterministic API that proves recurring-liability detection works on mock data — nothing more.

## Must Have

- Ingest a mock transaction dataset (Faker-generated) via a single API endpoint
- Deterministic recurring-bill detector: fixed-interval + fixed-amount matching (tolerance-based on amount and day-of-month/week cadence)
- Calculate a 14-day rolling Safe-to-Spend balance = ledger balance − upcoming detected liabilities in window
- `GET /safe-to-spend` endpoint returning current balance, detected upcoming bills, and next-bill date
- Dockerized, runnable locally with one command
- Basic input validation and error handling (malformed transaction data)

## Should Have

- Confidence score per detected recurring bill — **not completed, backlog**
- `/transactions/seed` endpoint to regenerate mock data on demand — **not completed, backlog**
- Unit tests covering the detection logic (core business risk area) — ✅ done (`app/tests/`)

## Could Have

- Configurable rolling window (7/14/30 days) via query param
- OpenAPI/Swagger docs polish for demo purposes
- Simple categorization tagging (e.g. "subscription" vs "utility")

## Won't Have (this PoC)

- Machine learning / statistical models for anomaly or pattern detection
- Real Open Banking (PSD2/OAuth) integrations
- Multi-currency or multi-account support
- User authentication / persistence beyond in-memory or mock DB
- Notifications, alerts, or push infrastructure
- Frontend UI

**Rationale:** Won't-Haves are excluded not for lack of value, but because they don't de-risk the core hypothesis — that deterministic pattern detection alone can produce a trustworthy forward-looking balance. ML and Open Banking are v2 investments once detection logic is validated.