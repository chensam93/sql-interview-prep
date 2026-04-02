"""
Generate sample data for Q001 (Lower): Conversion Funnel Basics.
Creates: data/duckdb/q001_lower.duckdb
"""

import duckdb
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(11)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q001_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists signups")
connection.execute("drop table if exists events")

start_date = date(2024, 1, 1)
end_date = date(2024, 3, 31)
channels = ["organic", "paid_search", "referral", "social"]
channel_weights = [0.4, 0.3, 0.2, 0.1]

signups = []
events = []

for user_number in range(900):
    user_id = f"user_{user_number:05d}"
    signup_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    acquisition_channel = random.choices(channels, channel_weights)[0]
    signups.append((user_id, signup_date, acquisition_channel))

    events.append((user_id, signup_date, "signup_complete"))

    if random.random() < 0.68:
        profile_date = signup_date + timedelta(days=random.randint(0, 12))
        events.append((user_id, profile_date, "profile_complete"))

    if random.random() < 0.36:
        purchase_date = signup_date + timedelta(days=random.randint(1, 28))
        events.append((user_id, purchase_date, "first_purchase"))

connection.execute(
    """
    create table signups (
        user_id varchar,
        signup_date date,
        acquisition_channel varchar
    )
    """
)
connection.executemany("insert into signups values (?, ?, ?)", signups)

connection.execute(
    """
    create table events (
        user_id varchar,
        event_date date,
        event_name varchar
    )
    """
)
connection.executemany("insert into events values (?, ?, ?)", events)

print(f"Created {database_path}")
