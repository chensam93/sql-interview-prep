"""
Generate sample data for Q005 (Lower): Inventory Snapshot Data Quality Checks.
Creates: data/duckdb/q005_lower.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q005_lower.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists stores")
connection.execute("drop table if exists inventory_snapshots")

stores = [
    ("store_001", "Downtown", "west"),
    ("store_002", "Uptown", "central"),
    ("store_003", "Airport", "east"),
]

products = ["prod_a", "prod_b", "prod_c", "prod_d"]
start_date = date(2024, 8, 1)
day_count = 14

inventory_snapshots = []
for day_offset in range(day_count):
    snapshot_date = start_date + timedelta(days=day_offset)
    for store_id, _, _ in stores:
        for product_index, product_id in enumerate(products):
            base_quantity = 40 + day_offset * 2 + product_index * 5
            store_adjustment = 0
            if store_id == "store_002":
                store_adjustment = 6
            if store_id == "store_003":
                store_adjustment = -4
            on_hand_qty = base_quantity + store_adjustment
            inventory_snapshots.append((store_id, product_id, snapshot_date, on_hand_qty))

# Inject known quality issues.
inventory_snapshots.append(("store_001", "prod_c", date(2024, 8, 4), -3))
inventory_snapshots.append(("store_003", "prod_a", date(2024, 8, 8), 650))
inventory_snapshots.append(("store_002", "prod_b", date(2024, 8, 10), 72))
inventory_snapshots.append(("store_002", "prod_b", date(2024, 8, 10), 72))
inventory_snapshots.append(("store_003", "prod_d", date(2024, 8, 12), 69))
inventory_snapshots.append(("store_003", "prod_d", date(2024, 8, 12), 69))

connection.execute(
    """
    create table stores (
        store_id varchar,
        store_name varchar,
        region varchar
    )
    """
)

connection.execute(
    """
    create table inventory_snapshots (
        store_id varchar,
        product_id varchar,
        snapshot_date date,
        on_hand_qty integer
    )
    """
)

connection.executemany("insert into stores values (?, ?, ?)", stores)
connection.executemany("insert into inventory_snapshots values (?, ?, ?, ?)", inventory_snapshots)

print(f"Created {database_path}")
