"""
Generate sample data for Q006 (Lower): Refund Without Return Event.
Creates: data/duckdb/q006_lower.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q006_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists orders")
connection.execute("drop table if exists order_events")

orders = []
order_events = []

start_date = date(2024, 9, 1)
for index in range(180):
    order_id = f"order_{index:05d}"
    customer_id = f"cust_{(index % 45) + 1:03d}"
    order_date = start_date + timedelta(days=index % 21)
    orders.append((order_id, customer_id, order_date))

    # Most orders have placed + shipped.
    order_events.append((order_id, order_date, "placed"))
    order_events.append((order_id, order_date + timedelta(days=1), "shipped"))

    # Many shipped orders are returned.
    if index % 4 != 0:
        order_events.append((order_id, order_date + timedelta(days=5), "returned"))

    # Some orders get refunds.
    if index % 3 == 0:
        order_events.append((order_id, order_date + timedelta(days=6), "refunded"))

# Inject explicit anomalies (refund but no return).
order_events.append(("order_00017", date(2024, 9, 11), "refunded"))
order_events.append(("order_00091", date(2024, 9, 15), "refunded"))
order_events.append(("order_00140", date(2024, 9, 19), "refunded"))

connection.execute(
    """
    create table orders (
        order_id varchar,
        customer_id varchar,
        order_date date
    )
    """
)

connection.execute(
    """
    create table order_events (
        order_id varchar,
        event_date date,
        event_type varchar
    )
    """
)

connection.executemany("insert into orders values (?, ?, ?)", orders)
connection.executemany("insert into order_events values (?, ?, ?)", order_events)

print(f"Created {database_path}")
connection.close()
