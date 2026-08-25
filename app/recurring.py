"""Deterministic recurring-bill detection and Safe-to-Spend calculation."""

from collections import defaultdict
from datetime import date, timedelta

TOLERANCE_DAYS = 4


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def detect_recurring_bills(transactions: list[dict]) -> list[dict]:
    """Group debits by (description, amount); flag groups whose occurrence
    intervals are consistent (within TOLERANCE_DAYS) as recurring liabilities."""
    groups: dict[tuple[str, float], list[str]] = defaultdict(list)
    for t in transactions:
        if t["type"] == "debit":
            groups[(t["description"], t["amount"])].append(t["date"])

    recurring = []
    for (description, amount), dates in groups.items():
        dates = sorted(dates)
        if len(dates) < 2:
            continue
        intervals = [(_parse(b) - _parse(a)).days for a, b in zip(dates, dates[1:])]
        avg_interval = sum(intervals) / len(intervals)
        if all(abs(i - avg_interval) <= TOLERANCE_DAYS for i in intervals):
            next_due = _parse(dates[-1]) + timedelta(days=round(avg_interval))
            recurring.append(
                {
                    "description": description,
                    "amount": amount,
                    "interval_days": round(avg_interval),
                    "last_date": dates[-1],
                    "next_due": next_due.isoformat(),
                }
            )
    return recurring


def safe_to_spend(transactions: list[dict], as_of: date, window_days: int = 14) -> dict:
    """Ledger balance minus recurring liabilities due within the rolling window."""
    balance = round(sum(t["amount"] for t in transactions), 2)
    window_end = as_of + timedelta(days=window_days)

    upcoming = [
        b
        for b in detect_recurring_bills(transactions)
        if as_of <= _parse(b["next_due"]) <= window_end
    ]
    upcoming_total = round(sum(b["amount"] for b in upcoming), 2)

    return {
        "as_of": as_of.isoformat(),
        "window_days": window_days,
        "ledger_balance": balance,
        "upcoming_liabilities": upcoming_total,
        "safe_to_spend": round(balance + upcoming_total, 2),
        "upcoming_bills": upcoming,
    }
