"""
Generate sample data for Q003 (Lower): Priority Mix by Channel.
Creates: data/duckdb/q003_lower.duckdb
"""

import random
from datetime import date, timedelta
from pathlib import Path

import duckdb

random.seed(37)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q003_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists tickets")

start_date = date(2024, 4, 1)
end_date = date(2024, 6, 30)

priorities = ["low", "medium", "high"]
source_channels = ["email", "chat", "phone"]
channel_weights = [0.5, 0.3, 0.2]

priority_weights_by_channel = {
    "email": [0.56, 0.29, 0.15],
    "chat": [0.48, 0.32, 0.20],
    "phone": [0.39, 0.33, 0.28],
}

tickets = []

for ticket_number in range(660):
    ticket_id = f"ticket_{ticket_number:05d}"
    opened_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    source_channel = random.choices(source_channels, channel_weights)[0]
    priority = random.choices(priorities, priority_weights_by_channel[source_channel])[0]
    tickets.append((ticket_id, opened_date, priority, source_channel))

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

print(f"Created {database_path}")
