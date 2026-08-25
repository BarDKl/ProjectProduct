# Safe-to-Spend Engine

A backend proof-of-concept that turns a static ledger balance into a forward-looking
**Safe-to-Spend** figure — ledger balance minus recurring liabilities (rent, subscriptions,
utilities) due in the next N days.

Built as a fintech Product Owner portfolio project: full problem framing → market research →
PRD → PoC implementation.

## Why

Bank apps show a static balance that doesn't distinguish money that's genuinely free to spend
from money already earmarked for upcoming bills. This PoC proves the core hypothesis —
that deterministic, zero-setup recurring-bill detection is enough to produce a trustworthy
forward-looking balance, with no ML or Open Banking integration required.

See [`ProductDocuments/`](./ProductDocuments) for the full Market Research Report, MVP Scope
(MoSCoW), and Product Requirements Document behind this build.

## How it works

1. Ingests a user's transaction history (synthetic data, generated via `Faker`, shaped like
   Open Banking transactions).
2. Groups debits by `(description, amount)` and flags a group as a recurring liability when its
   occurrence intervals are consistent within a tolerance window.
3. Projects each detected liability's next due date forward and sums those falling within the
   requested rolling window (default 14 days).
4. Returns `safe_to_spend = ledger_balance - upcoming_liabilities`, along with the itemized
   bills driving the deduction.

## Running it

**Docker (recommended):**

```bash
cd app
docker build -t safe-to-spend .
docker run -p 8000:8000 safe-to-spend
```

**Locally with [uv](https://github.com/astral-sh/uv):**

```bash
cd app
uv sync
uv run python data_generator.py   # generates synthetic_data.json
uv run uvicorn main:app --reload
```

API docs (Swagger UI) are then available at `http://localhost:8000/docs`.

## Running the tests

```bash
cd app
uv sync --group dev
uv run pytest
```

Tests cover the recurring-bill detector and Safe-to-Spend calculation, including the edge
cases called out in the PRD (insufficient history, variable-amount bills, false positives,
rolling-window boundary).

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check |
| `GET` | `/users` | List synthetic users |
| `GET` | `/users/{user_id}/transactions` | Raw transaction history for a user |
| `GET` | `/users/{user_id}/liabilities` | All detected recurring bills for a user |
| `GET` | `/users/{user_id}/balance/safe?window_days=14` | Safe-to-Spend balance + itemized upcoming bills |

## Project structure

```
app/
  main.py            FastAPI app and routes
  recurring.py        Recurring-bill detection + Safe-to-Spend calculation
  data_generator.py   Synthetic transaction dataset generator (Faker)
  tests/              Pytest suite for detection + Safe-to-Spend logic
  Dockerfile
ProductDocuments/
  Market Research Report.md
  MVP Scope.md
  Safe to Spend Product Requirements Document.md
```
