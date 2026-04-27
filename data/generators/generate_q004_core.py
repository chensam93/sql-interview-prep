"""
Generate sample data for Q004 (Core): Renewal Outcome Classification.
Creates: data/duckdb/q004_core.duckdb
"""

from datetime import date, timedelta
from pathlib import Path

import duckdb

database_path = Path(__file__).resolve().parent.parent / "duckdb" / "q004_core.duckdb"
database_path.parent.mkdir(parents=True, exist_ok=True)
connection = duckdb.connect(str(database_path))

connection.execute("drop table if exists invoices")
connection.execute("drop table if exists subscriptions")
connection.execute("drop table if exists accounts")

accounts = []
for account_number in range(1, 81):
    account_id = f"acct_{account_number:04d}"
    if account_number % 3 == 0:
        segment = "enterprise"
    elif account_number % 3 == 1:
        segment = "mid_market"
    else:
        segment = "smb"
    accounts.append((account_id, segment))

subscriptions = []
invoices = []

base_renewal_date = date(2024, 10, 20)
for subscription_number in range(1, 101):
    subscription_id = f"sub_{subscription_number:05d}"
    account_id = accounts[(subscription_number - 1) % len(accounts)][0]
    start_date = base_renewal_date - timedelta(days=180 + (subscription_number % 30))
    renewal_date = base_renewal_date + timedelta(days=(subscription_number % 45))
    status = "active" if subscription_number % 12 != 0 else "cancelled"
    subscriptions.append((subscription_id, account_id, start_date, renewal_date, status))

    # paid renewal invoice behavior
    pattern = subscription_number % 4
    if pattern == 0:
        paid_date = renewal_date + timedelta(days=2)   # on-time
    elif pattern == 1:
        paid_date = renewal_date + timedelta(days=10)  # late
    elif pattern == 2:
        paid_date = None                               # no paid renewal
    else:
        paid_date = renewal_date                       # exactly due date

    invoice_id = f"inv_{subscription_number:06d}"
    if paid_date is not None:
        invoices.append((invoice_id, subscription_id, paid_date, 1200 + (subscription_number % 6) * 100, "paid"))
    else:
        invoices.append((invoice_id, subscription_id, renewal_date + timedelta(days=3), 1200 + (subscription_number % 6) * 100, "void"))

    # occasional retry invoice rows
    if subscription_number % 10 == 0:
        retry_invoice_id = f"inv_retry_{subscription_number:06d}"
        invoices.append((retry_invoice_id, subscription_id, renewal_date + timedelta(days=6), 1200, "failed"))

connection.execute(
    """
    create table accounts (
        account_id varchar,
        segment varchar
    )
    """
)

connection.execute(
    """
    create table subscriptions (
        subscription_id varchar,
        account_id varchar,
        start_date date,
        renewal_date date,
        status varchar
    )
    """
)

connection.execute(
    """
    create table invoices (
        invoice_id varchar,
        subscription_id varchar,
        invoice_date date,
        amount numeric,
        invoice_status varchar
    )
    """
)

connection.executemany("insert into accounts values (?, ?)", accounts)
connection.executemany("insert into subscriptions values (?, ?, ?, ?, ?)", subscriptions)
connection.executemany("insert into invoices values (?, ?, ?, ?, ?)", invoices)

print(f"Created {database_path}")
connection.close()
