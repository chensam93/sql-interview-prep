"""
Generate sample data for Q007 (Lower): Trial Conversion Window Filter.
Creates: data/duckdb/q007_lower.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q007_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists trial_signups")
connection.execute("drop table if exists subscriptions")

trial_signups = []
subscriptions = []

start_date = date(2024, 10, 1)
for index in range(150):
    user_id = f"user_{index:04d}"
    signup_date = start_date + timedelta(days=index % 20)
    trial_signups.append((user_id, signup_date))

    # Conversion patterns to test boundary logic.
    if index % 5 == 0:
        subscriptions.append((user_id, signup_date + timedelta(days=0), "basic"))
    elif index % 5 == 1:
        subscriptions.append((user_id, signup_date + timedelta(days=7), "basic"))
    elif index % 5 == 2:
        subscriptions.append((user_id, signup_date + timedelta(days=8), "pro"))
    elif index % 5 == 3:
        subscriptions.append((user_id, signup_date + timedelta(days=3), "pro"))
    # index % 5 == 4 => never subscribed

# Explicit edge cases.
subscriptions.append(("user_0012", date(2024, 10, 13), "basic"))  # day 0 for that user
subscriptions.append(("user_0042", date(2024, 10, 30), "pro"))    # day 7 for that user

connection.execute(
    """
    create table trial_signups (
        user_id varchar,
        signup_date date
    )
    """
)

connection.execute(
    """
    create table subscriptions (
        user_id varchar,
        subscription_start_date date,
        plan_name varchar
    )
    """
)

connection.executemany("insert into trial_signups values (?, ?)", trial_signups)
connection.executemany("insert into subscriptions values (?, ?, ?)", subscriptions)

print(f"Created {database_path}")
connection.close()
