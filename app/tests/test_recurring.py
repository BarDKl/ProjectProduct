"""Tests for recurring-bill detection and Safe-to-Spend calculation.

Covers the edge cases called out in the PRD's Product Flow section (Section 7):
insufficient history, variable-amount bills, false positives, and the
rolling-window boundary.
"""

from datetime import date

import pytest

from recurring import detect_recurring_bills, safe_to_spend

RENT = [
    {"date": "2026-06-01", "amount": -2500.0, "type": "debit", "description": "Rent"},
    {"date": "2026-07-01", "amount": -2500.0, "type": "debit", "description": "Rent"},
    {"date": "2026-08-01", "amount": -2500.0, "type": "debit", "description": "Rent"},
]


def txn(d: str, amount: float, description: str, type_: str = "debit") -> dict:
    return {"date": d, "amount": amount, "type": type_, "description": description}


class TestDetectRecurringBills:
    def test_detects_consistent_monthly_bill(self):
        bills = detect_recurring_bills(RENT)
        assert len(bills) == 1
        assert bills[0]["description"] == "Rent"
        assert bills[0]["next_due"] == "2026-08-31"

    def test_single_occurrence_is_not_recurring(self):
        # PRD edge case: new user with insufficient transaction history.
        txns = [txn("2026-08-01", -2500.0, "Rent")]
        assert detect_recurring_bills(txns) == []

    def test_two_occurrences_are_sufficient_to_flag(self):
        # Current implementation's threshold is 2, not the PRD's stated 3
        # (US-2 acceptance criteria) — documents actual behavior.
        txns = [
            txn("2026-06-01", -2500.0, "Rent"),
            txn("2026-07-01", -2500.0, "Rent"),
        ]
        bills = detect_recurring_bills(txns)
        assert len(bills) == 1

    def test_irregular_intervals_are_not_flagged(self):
        # PRD edge case: false positive — coincidentally regular one-off
        # spending should not be misclassified as recurring.
        txns = [
            txn("2026-06-01", -40.0, "Cafe"),
            txn("2026-06-11", -40.0, "Cafe"),
            txn("2026-07-25", -40.0, "Cafe"),
        ]
        assert detect_recurring_bills(txns) == []

    def test_variable_amount_bill_is_not_grouped(self):
        # PRD edge case: recurring bill with a variable amount (e.g. utilities).
        # Detection groups by exact (description, amount), so amount drift
        # breaks grouping entirely — no amount tolerance is currently applied.
        txns = [
            txn("2026-06-20", -129.00, "Internet & Phone"),
            txn("2026-07-20", -131.50, "Internet & Phone"),
            txn("2026-08-20", -128.75, "Internet & Phone"),
        ]
        assert detect_recurring_bills(txns) == []

    def test_credits_are_ignored(self):
        txns = [
            txn("2026-06-01", 3000.0, "Salary", type_="credit"),
            txn("2026-07-01", 3000.0, "Salary", type_="credit"),
        ]
        assert detect_recurring_bills(txns) == []

    def test_multiple_distinct_bills_detected_independently(self):
        netflix = [
            txn("2026-06-15", -49.99, "Netflix"),
            txn("2026-07-15", -49.99, "Netflix"),
            txn("2026-08-15", -49.99, "Netflix"),
        ]
        bills = detect_recurring_bills(RENT + netflix)
        descriptions = {b["description"] for b in bills}
        assert descriptions == {"Rent", "Netflix"}


class TestSafeToSpend:
    def test_balance_and_upcoming_deduction(self):
        txns = RENT + [
            txn("2026-08-10", -30.0, "Coffee"),
            txn("2026-08-20", 3000.0, "Salary", type_="credit"),
        ]
        result = safe_to_spend(txns, as_of=date(2026, 8, 15), window_days=20)
        assert result["ledger_balance"] == round(3000 - 2500 * 3 - 30, 2)
        assert result["upcoming_liabilities"] == -2500.0
        assert result["safe_to_spend"] == round(result["ledger_balance"] - 2500.0, 2)

    def test_no_transactions_yields_zero_balance(self):
        result = safe_to_spend([], as_of=date(2026, 8, 15))
        assert result["ledger_balance"] == 0
        assert result["safe_to_spend"] == 0
        assert result["upcoming_bills"] == []

    def test_bill_due_exactly_on_window_boundary_is_included(self):
        # PRD edge case: liability due exactly on day 14 of the rolling window.
        txns = RENT
        as_of = date(2026, 8, 17)
        window_days = (date(2026, 8, 31) - as_of).days  # next_due lands exactly on window_end
        result = safe_to_spend(txns, as_of=as_of, window_days=window_days)
        assert result["upcoming_liabilities"] == -2500.0

    def test_bill_due_one_day_past_window_is_excluded(self):
        txns = RENT
        as_of = date(2026, 8, 17)
        window_days = (date(2026, 8, 31) - as_of).days - 1
        result = safe_to_spend(txns, as_of=as_of, window_days=window_days)
        assert result["upcoming_liabilities"] == 0
        assert result["upcoming_bills"] == []
