"""
Generate sample data for Q002 (Lower): 7-Day Resolution Rate by Channel.
Creates: data/duckdb/q002_lower.duckdb
"""

import random
from datetime import date, timedelta
from pathlib import Path

import duckdb

random.seed(31)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q002_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists tickets")
connection.execute("drop table if exists ticket_updates")

start_date = date(2024, 3, 1)
end_date = date(2024, 5, 31)

priorities = ["low", "medium", "high"]
priority_weights = [0.45, 0.35, 0.20]

source_channels = ["email", "chat", "phone"]
source_weights = [0.52, 0.30, 0.18]

tickets = []
ticket_updates = []

for ticket_number in range(720):
    ticket_id = f"ticket_{ticket_number:05d}"
    opened_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    priority = random.choices(priorities, priority_weights)[0]
    source_channel = random.choices(source_channels, source_weights)[0]

    tickets.append((ticket_id, opened_date, priority, source_channel))

    if random.random() < 0.75:
        comment_date = opened_date + timedelta(days=random.randint(0, 4))
        ticket_updates.append((ticket_id, comment_date, "comment"))

    resolved_probability_by_channel = {
        "email": 0.62,
        "chat": 0.74,
        "phone": 0.56,
    }

    if random.random() < resolved_probability_by_channel[source_channel]:
        resolution_date = opened_date + timedelta(days=random.randint(0, 10))
        ticket_updates.append((ticket_id, resolution_date, "resolved"))

connection.execute(
    """
    create table tickets (
        ticket_id varchar,
        opened_date date,
        priority varchar,
        source_channel varchar
    )
    """
)
connection.executemany("insert into tickets values (?, ?, ?, ?)", tickets)

connection.execute(
    """
    create table ticket_updates (
        ticket_id varchar,
        update_date date,
        update_type varchar
    )
    """
)
connection.executemany("insert into ticket_updates values (?, ?, ?)", ticket_updates)

print(f"Created {database_path}")
