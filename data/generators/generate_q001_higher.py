"""
Generate sample data for Q001 (Higher): Subscription MRR Movements.
Creates: data/duckdb/q001_higher.duckdb
"""

import duckdb
import random
from datetime import date
from pathlib import Path

random.seed(21)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q001_higher.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists subscription_snapshots")

months = [
    date(2024, 1, 1),
    date(2024, 2, 1),
    date(2024, 3, 1),
    date(2024, 4, 1),
    date(2024, 5, 1),
    date(2024, 6, 1),
]

snapshots = []

for account_number in range(220):
    account_id = f"acct_{account_number:04d}"
    active = random.random() < 0.72
    mrr = random.choice([49, 79, 129, 199, 299]) if active else 0

    for month in months:
        if active and random.random() < 0.08:
            mrr = 0
            active = False
        elif not active and random.random() < 0.12:
            active = True
            mrr = random.choice([49, 79, 129, 199, 299])
        elif active:
            mrr = max(0, mrr + random.choice([-50, -20, 0, 10, 25, 40]))

        snapshots.append((month, account_id, float(mrr)))

connection.execute(
    """
    create table subscription_snapshots (
        snapshot_month date,
        account_id varchar,
        mrr numeric
    )
    """
)
connection.executemany("insert into subscription_snapshots values (?, ?, ?)", snapshots)

print(f"Created {database_path}")
