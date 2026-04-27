"""
Generate sample data for Q005 (Core): Overlapping Subscription Periods Audit.
Creates: data/duckdb/q005_core.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q005_core.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists account_subscriptions")

rows = []
base_date = date(2023, 1, 1)

# Mostly clean data: one plan period at a time per account.
for account_number in range(1, 71):
    account_id = f"acct_{account_number:04d}"
    cycle_count = 2 + (account_number % 3)
    cycle_start = base_date + timedelta(days=account_number * 2)
    for cycle in range(cycle_count):
        subscription_id = f"sub_{account_number:04d}_{cycle+1:02d}"
        start_date = cycle_start + timedelta(days=cycle * 90)
        end_date = start_date + timedelta(days=89)
        plan_name = "pro" if cycle % 2 == 0 else "basic"
        rows.append((account_id, subscription_id, start_date, end_date, plan_name))

# Inject overlap anomalies.
rows.extend(
    [
        ("acct_0007", "sub_0007_ov1", date(2024, 2, 1), date(2024, 4, 15), "pro"),
        ("acct_0007", "sub_0007_ov2", date(2024, 3, 20), date(2024, 6, 1), "enterprise"),
        ("acct_0021", "sub_0021_ov1", date(2024, 1, 10), date(2024, 2, 28), "basic"),
        ("acct_0021", "sub_0021_ov2", date(2024, 2, 15), date(2024, 5, 10), "pro"),
        ("acct_0044", "sub_0044_ov1", date(2024, 5, 1), date(2024, 7, 20), "pro"),
        ("acct_0044", "sub_0044_ov2", date(2024, 5, 15), date(2024, 8, 31), "pro_plus"),
        ("acct_0069", "sub_0069_ov1", date(2024, 6, 1), date(2024, 6, 30), "basic"),
        ("acct_0069", "sub_0069_ov2", date(2024, 6, 30), date(2024, 9, 1), "pro"),
    ]
)

connection.execute(
    """
    create table account_subscriptions (
        account_id varchar,
        subscription_id varchar,
        start_date date,
        end_date date,
        plan_name varchar
    )
    """
)
connection.executemany("insert into account_subscriptions values (?, ?, ?, ?, ?)", rows)

print(f"Created {database_path}")
connection.close()
connection.close()
