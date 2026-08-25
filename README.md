# Safe-to-Spend Engine

A portfolio project for the **Technical Product Owner** track: end-to-end problem
framing, market research, a PRD, and a working PoC for a fintech feature.

**The idea:** bank apps show a static balance that ignores upcoming bills (rent,
subscriptions, utilities), so people misjudge what they can actually spend. This
PoC deducts detected recurring bills from the balance to show a trustworthy
**Safe-to-Spend** number — no ML, no bank integration, just deterministic rules.

## Product docs

| Doc | What's in it |
| --- | --- |
| [Market Research Report](https://app.notion.com/p/3ba32be71aab80e2a209de22783f458c) | The problem, competitor benchmarking, evidence |
| [Product Requirements Document](https://app.notion.com/p/ced32be71aab82bbb77501fd741b9510) | Objective, OKRs, personas, user stories, solution |
| [MVP Scope](https://app.notion.com/p/3ba32be71aab800c9054c4e19c864eba) | MoSCoW scope for the PoC build |
| [PoC Report](https://app.notion.com/p/3ba32be71aab80579d7ef145aa2b9481) | What was built, proof it works, next steps |

## How it works

1. Ingest a user's transaction history (synthetic, generated with `Faker`).
2. Detect recurring bills — same payee, same amount, consistent interval.
3. Project each bill's next due date and sum those falling in the next 14 days.
4. Return `safe_to_spend = ledger_balance − upcoming_liabilities`, with the
   itemized bills behind that number.

## Running it

```bash
cd app
docker build -t safe-to-spend . && docker run -p 8000:8000 safe-to-spend
```

Or locally with [uv](https://github.com/astral-sh/uv):

```bash
cd app
uv sync
uv run python data_generator.py   # generates synthetic_data.json
uv run uvicorn main:app --reload
```

Swagger docs: `http://localhost:8000/docs`. Tests: `uv run pytest` (after `uv sync --group dev`).

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness check |
| `GET` | `/users` | List synthetic users |
| `GET` | `/users/{user_id}/transactions` | Raw transaction history |
| `GET` | `/users/{user_id}/liabilities` | Detected recurring bills |
| `GET` | `/users/{user_id}/balance/safe?window_days=14` | Safe-to-Spend balance + itemized bills |

## Stack

Python 3.12, FastAPI, Docker. `app/` holds the service; `ProductDocuments/` holds
local copies of the docs above.
