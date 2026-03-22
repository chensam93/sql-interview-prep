"""
Generate sample data for Q001: Cohort Retention Analysis.
Run from repo root:
    python data/generate_q001.py
Creates: data/q001.duckdb
"""

import duckdb
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).parent / "q001.duckdb"
if DB_PATH.exists():
    DB_PATH.unlink()

conn = duckdb.connect(str(DB_PATH))

START_DATE = date(2024, 10, 1)
END_DATE   = date(2024, 12, 31)
N_USERS    = 1500

CHANNELS   = ["organic", "paid_social", "referral"]
PLAN_TYPES = ["free", "premium"]
CHANNEL_WEIGHTS  = [0.5, 0.3, 0.2]
PLAN_WEIGHTS     = [0.7, 0.3]
ACTIVITY_TYPES   = ["login", "feature_use", "purchase"]
ACTIVITY_WEIGHTS = [0.5, 0.35, 0.15]

def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# ── users ─────────────────────────────────────────────────────────────────────
users = []
for i in range(N_USERS):
    users.append({
        "user_id":     f"user_{i:04d}",
        "signup_date": rand_date(START_DATE, END_DATE - timedelta(days=35)),
        "channel":     random.choices(CHANNELS, CHANNEL_WEIGHTS)[0],
        "plan_type":   random.choices(PLAN_TYPES, PLAN_WEIGHTS)[0],
    })

# ── activity ──────────────────────────────────────────────────────────────────
activity = []
for u in users:
    signup = u["signup_date"]
    is_premium = u["plan_type"] == "premium"

    # base retention probabilities
    p_d1  = 0.55 if is_premium else 0.35
    p_d7  = 0.40 if is_premium else 0.22
    p_d30 = 0.25 if is_premium else 0.12

    # guarantee milestone-day activity for retained users
    for offset, prob in [(1, p_d1), (7, p_d7), (30, p_d30)]:
        activity_date = signup + timedelta(days=offset)
        if activity_date <= END_DATE and random.random() < prob:
            activity.append({
                "user_id":       u["user_id"],
                "activity_date": activity_date,
                "activity_type": random.choices(ACTIVITY_TYPES, ACTIVITY_WEIGHTS)[0],
            })

    # random background activity (0–8 sessions) over first 45 days
    n_sessions = random.randint(0, 8)
    max_offset = min(45, (END_DATE - signup).days)
    for _ in range(n_sessions):
        offset = random.randint(0, max_offset)
        activity.append({
            "user_id":       u["user_id"],
            "activity_date": signup + timedelta(days=offset),
            "activity_type": random.choices(ACTIVITY_TYPES, ACTIVITY_WEIGHTS)[0],
        })

# ── write to duckdb ───────────────────────────────────────────────────────────
conn.execute("""
    create table users (
        user_id      varchar,
        signup_date  date,
        channel      varchar,
        plan_type    varchar
    )
""")
conn.executemany(
    "insert into users values (?, ?, ?, ?)",
    [(u["user_id"], u["signup_date"], u["channel"], u["plan_type"]) for u in users],
)

conn.execute("""
    create table activity (
        user_id       varchar,
        activity_date date,
        activity_type varchar
    )
""")
conn.executemany(
    "insert into activity values (?, ?, ?)",
    [(a["user_id"], a["activity_date"], a["activity_type"]) for a in activity],
)

# quick sanity
n_users    = conn.execute("select count(*) from users").fetchone()[0]
n_activity = conn.execute("select count(*) from activity").fetchone()[0]
n_cohorts  = conn.execute(
    "select count(distinct date_trunc('week', signup_date)) from users"
).fetchone()[0]

conn.close()
print(f"Created {DB_PATH}")
print(f"  users:    {n_users}")
print(f"  activity: {n_activity}")
print(f"  cohort weeks: {n_cohorts}")
