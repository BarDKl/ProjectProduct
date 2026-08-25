#!/usr/bin/env python3.12
"""
Safe-to-Spend Data Generator
Generates synthetic transaction data for 5 users with recurring bills and daily noise.
"""

from faker import Faker
from datetime import datetime, timedelta
import random
import json
from typing import TypedDict

fake = Faker('pl_PL')
random.seed(42)

class Transaction(TypedDict):
    date: str
    amount: float
    type: str
    category: str
    description: str

class User(TypedDict):
    user_id: str
    name: str
    email: str
    transactions: list[Transaction]

def generate_users(count: int = 5) -> list[str]:
    """Generate unique user identifiers."""
    return [f"USER_{i+1:05d}" for i in range(count)]

def generate_fixed_bills(user_id: str) -> list[dict]:
    """Generate 3 fixed monthly bills per user."""
    bills = [
        {
            "date": 1,  # Day of month
            "amount": 2500.0,
            "category": "Housing",
            "description": "Rent"
        },
        {
            "date": 15,
            "amount": 49.99,
            "category": "Subscription",
            "description": "Netflix"
        },
        {
            "date": 20,
            "amount": 129.00,
            "category": "Utilities",
            "description": "Internet & Phone"
        }
    ]
    return bills

def generate_salary_deposits(user_id: str, start_date: datetime, end_date: datetime) -> list[Transaction]:
    """Generate bi-weekly 3,000 PLN salary deposits."""
    transactions = []
    current_date = start_date

    while current_date <= end_date:
        transactions.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "amount": 3000.0,
            "type": "credit",
            "category": "Income",
            "description": "Salary"
        })
        current_date += timedelta(days=14)

    return transactions

def generate_fixed_bill_transactions(
    user_id: str,
    bills: list[dict],
    start_date: datetime,
    end_date: datetime
) -> list[Transaction]:
    """Generate recurring bill transactions for each month in range."""
    transactions = []
    current_date = start_date

    while current_date <= end_date:
        for bill in bills:
            bill_date = current_date.replace(day=min(bill["date"], 28))

            if start_date <= bill_date <= end_date:
                transactions.append({
                    "date": bill_date.strftime("%Y-%m-%d"),
                    "amount": -bill["amount"],
                    "type": "debit",
                    "category": bill["category"],
                    "description": bill["description"]
                })

        current_date += timedelta(days=30)

    return transactions

def generate_daily_noise(
    user_id: str,
    count: int = 20,
    start_date: datetime = None,
    end_date: datetime = None
) -> list[Transaction]:
    """Generate randomized daily transactions (noise)."""
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()

    categories = ["Groceries", "Dining", "Transport", "Entertainment", "Shopping", "Healthcare"]
    descriptions = [
        "Supermarket", "Restaurant", "Gas", "Cinema", "Clothing", "Pharmacy",
        "Cafe", "Taxi", "Books", "Gym", "Haircut", "Electronics"
    ]

    transactions = []
    day_range = (end_date - start_date).days

    for _ in range(count):
        random_days = random.randint(0, day_range)
        transaction_date = start_date + timedelta(days=random_days)
        amount = round(random.uniform(5.0, 200.0), 2)

        transactions.append({
            "date": transaction_date.strftime("%Y-%m-%d"),
            "amount": -amount,
            "type": "debit",
            "category": random.choice(categories),
            "description": random.choice(descriptions)
        })

    return transactions

def generate_user_dataset(user_ids: list[str], months: int = 1) -> list[User]:
    """Generate complete dataset for all users."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * months)

    dataset = []

    for user_id in user_ids:
        salary_txns = generate_salary_deposits(user_id, start_date, end_date)
        bills = generate_fixed_bills(user_id)
        bill_txns = generate_fixed_bill_transactions(user_id, bills, start_date, end_date)
        noise_txns = generate_daily_noise(user_id, count=20, start_date=start_date, end_date=end_date)

        all_transactions = salary_txns + bill_txns + noise_txns
        all_transactions.sort(key=lambda x: x["date"])

        dataset.append({
            "user_id": user_id,
            "name": fake.name(),
            "email": fake.email(),
            "transactions": all_transactions
        })

    return dataset

def main():
    """Generate and output synthetic dataset."""
    user_ids = generate_users(count=5)
    dataset = generate_user_dataset(user_ids, months=3)

    output = {
        "generated_at": datetime.now().isoformat(),
        "user_count": len(dataset),
        "users": dataset
    }

    with open("synthetic_data.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✓ Dataset generated: {len(dataset)} users")
    print(f"✓ Output: synthetic_data.json")
    print(f"✓ Total transactions: {sum(len(u['transactions']) for u in dataset)}")

if __name__ == "__main__":
    main()
