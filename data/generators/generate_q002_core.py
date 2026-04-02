"""
Generate sample data for Q002 (Core): Channel Revenue Mix (New vs Returning).
Creates: data/duckdb/q002_core.duckdb
"""

import duckdb
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(29)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q002_core.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists orders")
connection.execute("drop table if exists order_items")

start_date = date(2024, 1, 1)
end_date = date(2024, 9, 30)
channels = ["organic", "paid_search", "email", "affiliate"]
channel_weights = [0.36, 0.33, 0.21, 0.10]
products = ["prod_a", "prod_b", "prod_c", "prod_d", "prod_e", "prod_f"]
base_price = {
    "prod_a": 18.0,
    "prod_b": 32.0,
    "prod_c": 48.0,
    "prod_d": 75.0,
    "prod_e": 110.0,
    "prod_f": 155.0,
}

orders = []
order_items = []
order_count = 900
customer_pool = [f"cust_{index:04d}" for index in range(1, 320)]

for order_number in range(order_count):
    order_id = f"order_{order_number:05d}"
    customer_id = random.choice(customer_pool)
    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    channel = random.choices(channels, channel_weights)[0]
    orders.append((order_id, customer_id, order_date, channel))

    item_count = random.randint(1, 4)
    selected_products = random.sample(products, k=item_count)
    for product_id in selected_products:
        quantity = random.randint(1, 4)
        unit_price = base_price[product_id] + random.choice([-2.0, 0.0, 0.0, 3.0, 5.0])
        order_items.append((order_id, product_id, quantity, unit_price))

connection.execute(
    """
    create table orders (
        order_id varchar,
        customer_id varchar,
        order_date date,
        channel varchar
    )
    """
)
connection.executemany("insert into orders values (?, ?, ?, ?)", orders)

connection.execute(
    """
    create table order_items (
        order_id varchar,
        product_id varchar,
        quantity integer,
        unit_price numeric
    )
    """
)
connection.executemany("insert into order_items values (?, ?, ?, ?)", order_items)

print(f"Created {database_path}")
