"""
Generate sample data for Q004 (Lower): Carrier On-Time Delivery Basics.
Creates: data/duckdb/q004_lower.duckdb
"""

import random
from datetime import date, timedelta
from pathlib import Path

import duckdb

random.seed(44)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q004_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists shipments")
connection.execute("drop table if exists shipment_events")

start_date = date(2024, 5, 1)
end_date = date(2024, 7, 31)

carriers = ["parcel_fast", "postal_economy", "regional_ground"]
carrier_weights = [0.35, 0.30, 0.35]
promised_days_by_carrier = {
    "parcel_fast": 2,
    "regional_ground": 4,
    "postal_economy": 6,
}
delivery_probability_by_carrier = {
    "parcel_fast": 0.95,
    "regional_ground": 0.87,
    "postal_economy": 0.76,
}
delay_distribution_by_carrier = {
    "parcel_fast": [-1, 0, 0, 1, 2],
    "regional_ground": [-1, 0, 1, 2, 3],
    "postal_economy": [0, 1, 2, 3, 4],
}

shipments = []
shipment_events = []

for shipment_number in range(540):
    shipment_id = f"shipment_{shipment_number:05d}"
    ship_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    carrier = random.choices(carriers, carrier_weights)[0]
    promised_date = ship_date + timedelta(days=promised_days_by_carrier[carrier])

    shipments.append((shipment_id, ship_date, carrier, promised_date))

    if random.random() < 0.22:
        exception_date = ship_date + timedelta(days=random.randint(0, 3))
        shipment_events.append((shipment_id, exception_date, "exception"))

    if random.random() < delivery_probability_by_carrier[carrier]:
        delay_days = random.choice(delay_distribution_by_carrier[carrier])
        delivered_date = promised_date + timedelta(days=delay_days)
        delivered_date = max(delivered_date, ship_date)
        shipment_events.append((shipment_id, delivered_date, "delivered"))

connection.execute(
    """
    create table shipments (
        shipment_id varchar,
        ship_date date,
        carrier varchar,
        promised_date date
    )
    """
)

connection.execute(
    """
    create table shipment_events (
        shipment_id varchar,
        event_date date,
        event_type varchar
    )
    """
)

connection.executemany("insert into shipments values (?, ?, ?, ?)", shipments)
connection.executemany("insert into shipment_events values (?, ?, ?)", shipment_events)

print(f"Created {database_path}")
