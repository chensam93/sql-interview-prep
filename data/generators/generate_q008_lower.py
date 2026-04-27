"""
Generate sample data for Q008 (Lower): Failed Logins Before First Success.
Creates: data/duckdb/q008_lower.duckdb
"""

from datetime import datetime, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q008_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists auth_events")

base_time = datetime(2024, 11, 1, 8, 0, 0)
auth_events = []

for index in range(90):
    user_id = f"user_{index:04d}"
    start_time = base_time + timedelta(minutes=index * 11)

    pattern = index % 5
    if pattern == 0:
        event_types = ["failed_login", "failed_login", "failed_login", "successful_login"]
    elif pattern == 1:
        event_types = ["failed_login", "failed_login", "successful_login"]
    elif pattern == 2:
        event_types = ["failed_login", "successful_login"]
    elif pattern == 3:
        event_types = ["successful_login"]
    else:
        event_types = ["failed_login", "failed_login", "failed_login", "failed_login", "successful_login"]

    for step_index, event_type in enumerate(event_types):
        auth_events.append((user_id, start_time + timedelta(minutes=step_index), event_type))

# Explicit edge cases for clarity.
auth_events.extend(
    [
        ("user_0095", datetime(2024, 11, 3, 10, 0, 0), "failed_login"),
        ("user_0095", datetime(2024, 11, 3, 10, 1, 0), "failed_login"),
        ("user_0095", datetime(2024, 11, 3, 10, 2, 0), "failed_login"),
        ("user_0095", datetime(2024, 11, 3, 10, 3, 0), "successful_login"),
        ("user_0096", datetime(2024, 11, 3, 10, 4, 0), "failed_login"),
        ("user_0096", datetime(2024, 11, 3, 10, 5, 0), "successful_login"),
    ]
)

connection.execute(
    """
    create table auth_events (
        user_id varchar,
        event_time timestamp,
        event_type varchar
    )
    """
)

connection.executemany("insert into auth_events values (?, ?, ?)", auth_events)

print(f"Created {database_path}")
connection.close()
