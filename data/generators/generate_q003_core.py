"""
Generate sample data for Q003 (Core): Monthly gross vs refunds (net revenue).
Creates: data/duckdb/q003_core.duckdb
"""

import duckdb
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(41)

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q003_core.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists returns")
connection.execute("drop table if exists orders")
connection.execute("drop table if exists order_items")

start_date = date(2024, 1, 1)
end_date = date(2024, 6, 30)
channel_values = ["organic", "paid_search", "email"]
channel_weights = [0.42, 0.38, 0.20]

product_values = ["prod_a", "prod_b", "prod_c", "prod_d"]
price_by_product = {
    "prod_a": 22.0,
    "prod_b": 44.0,
    "prod_c": 68.0,
    "prod_d": 95.0,
}

orders = []
order_items = []
order_count = 520

for order_number in range(order_count):
    order_id = f"order_{order_number:05d}"
    customer_id = f"cust_{random.randint(1, 180):04d}"
    day_offset = random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=day_offset)
    channel = random.choices(channel_values, channel_weights)[0]

    orders.append((order_id, customer_id, order_date, channel))

    line_item_count = random.randint(1, 3)
    selected_products = random.sample(product_values, k=line_item_count)
    for product_id in selected_products:
        quantity = random.randint(1, 3)
        unit_price = price_by_product[product_id] + random.choice([0.0, 0.0, 2.0, -1.5])
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

order_revenue_rows = connection.execute(
    """
    select
        orders.order_id,
        orders.order_date,
        sum(order_items.quantity * order_items.unit_price) as order_gross
    from orders
    inner join order_items
        on order_items.order_id = orders.order_id
    group by
        orders.order_id,
        orders.order_date
    """
).fetchall()

returns_rows = []
return_counter = 0
for order_id, order_date, order_gross in order_revenue_rows:
    if random.random() > 0.12:
        continue
    return_counter += 1
    return_id = f"ret_{return_counter:05d}"
    days_after = random.randint(0, min(45, (end_date - order_date).days))
    return_date = order_date + timedelta(days=days_after)
    if return_date > end_date:
        return_date = end_date
    refund_fraction = random.choice([0.25, 0.5, 1.0])
    refund_amount = round(float(order_gross) * refund_fraction, 2)
    returns_rows.append((return_id, order_id, return_date, refund_amount))

connection.execute(
    """
    create table returns (
        return_id varchar,
        order_id varchar,
        return_date date,
        refund_amount numeric
    )
    """
)
connection.executemany("insert into returns values (?, ?, ?, ?)", returns_rows)

print(f"Created {database_path}")
