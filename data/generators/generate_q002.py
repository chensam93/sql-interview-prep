"""
Generate sample data for Q002: Monthly Revenue Trends.

Run directly:
    python data/generators/generate_q002.py
Or build every question at once:
    python data/bootstrap.py

Creates: data/q002.duckdb
"""

import duckdb
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(7)

DATABASE_PATH = Path(__file__).resolve().parent.parent / "q002.duckdb"
connection = duckdb.connect(str(DATABASE_PATH))

connection.execute("drop table if exists orders")
connection.execute("drop table if exists order_items")

start_date = date(2024, 1, 1)
end_date = date(2024, 6, 30)
channel_values = ["organic", "paid_search", "email"]
channel_weights = [0.45, 0.35, 0.20]

product_values = ["prod_a", "prod_b", "prod_c", "prod_d", "prod_e"]
price_by_product = {
    "prod_a": 19.0,
    "prod_b": 35.0,
    "prod_c": 49.0,
    "prod_d": 79.0,
    "prod_e": 129.0,
}

orders = []
order_items = []
order_count = 600

for order_number in range(order_count):
    order_id = f"order_{order_number:05d}"
    customer_id = f"cust_{random.randint(1, 220):04d}"
    day_offset = random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=day_offset)
    channel = random.choices(channel_values, channel_weights)[0]

    orders.append((order_id, customer_id, order_date, channel))

    line_item_count = random.randint(1, 3)
    selected_products = random.sample(product_values, k=line_item_count)
    for product_id in selected_products:
        quantity = random.randint(1, 4)
        unit_price = price_by_product[product_id] + random.choice([0.0, 0.0, 2.0, -1.0])
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

order_total = connection.execute("select count(*) from orders").fetchone()[0]
line_item_total = connection.execute("select count(*) from order_items").fetchone()[0]
month_total = connection.execute(
    "select count(distinct date_trunc('month', order_date)) from orders"
).fetchone()[0]

connection.close()
print(f"Created {DATABASE_PATH}")
print(f"  orders: {order_total}")
print(f"  order_items: {line_item_total}")
print(f"  months: {month_total}")
