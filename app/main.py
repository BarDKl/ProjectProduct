"""Safe-to-Spend Engine — FastAPI service entrypoint."""

import json
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException

from recurring import detect_recurring_bills, safe_to_spend

DATA_FILE = Path(__file__).parent / "synthetic_data.json"

app = FastAPI(
    title="Safe-to-Spend Engine",
    description="Predicts a user's forward-looking safe-to-spend balance over a 14-day rolling window.",
    version="0.1.0",
)


def load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def load_users() -> dict[str, dict]:
    return {user["user_id"]: user for user in load_data()["users"]}


def get_user_or_404(user_id: str) -> dict:
    users = load_users()
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict]:
    users = load_users()
    return [
        {"user_id": u["user_id"], "name": u["name"], "email": u["email"]}
        for u in users.values()
    ]


@app.get("/users/{user_id}/transactions")
def get_transactions(user_id: str) -> list[dict]:
    return get_user_or_404(user_id)["transactions"]


@app.get("/users/{user_id}/liabilities")
def get_liabilities(user_id: str) -> list[dict]:
    """All detected recurring bills for the user, regardless of due date."""
    return detect_recurring_bills(get_user_or_404(user_id)["transactions"])


@app.get("/users/{user_id}/balance/safe")
def get_safe_to_spend(user_id: str, window_days: int = 14) -> dict:
    """Ledger balance minus recurring liabilities due within the rolling window."""
    transactions = get_user_or_404(user_id)["transactions"]
    as_of = datetime.fromisoformat(load_data()["generated_at"]).date()
    return safe_to_spend(transactions, as_of=as_of, window_days=window_days)
