"""
Run bucketed solution SQL files against local DuckDB files and write a markdown log.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import duckdb


REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO_ROOT / "validation" / "solution_validation_log.md"


def _split_sql_statements(sql_text: str) -> list[str]:
    parts = [part.strip() for part in sql_text.split(";")]
    return [part for part in parts if part]


def _format_rows(columns: list[str], rows: list[tuple], limit: int = 5) -> str:
    preview = rows[:limit]
    lines = [", ".join(columns)]
    for row in preview:
        lines.append(", ".join(str(value) for value in row))
    if len(rows) > limit:
        lines.append(f"... ({len(rows) - limit} more rows)")
    return "\n".join(lines)


def _run_solution(database_path: Path, solution_path: Path) -> list[dict]:
    sql_text = solution_path.read_text(encoding="utf-8")
    statements = _split_sql_statements(sql_text)
    results: list[dict] = []

    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        for statement_number, statement in enumerate(statements, start=1):
            cursor = connection.execute(statement)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            results.append(
                {
                    "statement_number": statement_number,
                    "row_count": len(rows),
                    "columns": columns,
                    "preview": _format_rows(columns, rows),
                }
            )
    finally:
        connection.close()

    return results


def _run_invariant_checks() -> dict[str, str]:
    checks: dict[str, str] = {}

    core_db = REPO_ROOT / "data" / "duckdb" / "q001_core.duckdb"
    lower_db = REPO_ROOT / "data" / "duckdb" / "q001_lower.duckdb"
    higher_db = REPO_ROOT / "data" / "duckdb" / "q001_higher.duckdb"

    core_conn = duckdb.connect(str(core_db), read_only=True)
    try:
        month_count = core_conn.execute(
            "select count(distinct date_trunc('month', order_date)::date) from orders"
        ).fetchone()[0]
        checks["core"] = f"Distinct months in raw data: {month_count}"
    finally:
        core_conn.close()

    lower_conn = duckdb.connect(str(lower_db), read_only=True)
    try:
        violations = lower_conn.execute(
            """
            with signups_with_events as (
                select
                    signups.user_id,
                    date_trunc('week', signups.signup_date)::date as signup_week,
                    max(
                        case when events.event_name = 'first_purchase'
                            and events.event_date <= signups.signup_date + interval '30 day'
                        then 1 else 0 end
                    ) as has_purchase
                from signups
                left join events
                    on events.user_id = signups.user_id
                   and events.event_date >= signups.signup_date
                group by
                    signups.user_id,
                    date_trunc('week', signups.signup_date)::date
            ),
            weekly as (
                select
                    signup_week,
                    count(*) as signed_up_users,
                    sum(has_purchase) as purchased_users
                from signups_with_events
                group by signup_week
            )
            select count(*)
            from weekly
            where purchased_users > signed_up_users
            """
        ).fetchone()[0]
        checks["lower"] = f"Weeks with purchased_users > signed_up_users: {violations}"
    finally:
        lower_conn.close()

    higher_conn = duckdb.connect(str(higher_db), read_only=True)
    try:
        movement_mismatches = higher_conn.execute(
            """
            with account_monthly_mrr as (
                select
                    snapshot_month,
                    account_id,
                    mrr as current_mrr,
                    coalesce(
                        lag(mrr) over (
                            partition by account_id
                            order by snapshot_month
                        ),
                        0
                    ) as prior_mrr
                from subscription_snapshots
            ),
            classified as (
                select
                    snapshot_month,
                    prior_mrr,
                    current_mrr,
                    case when prior_mrr = 0 and current_mrr > 0 then current_mrr else 0 end as new_mrr,
                    case when prior_mrr > 0 and current_mrr > prior_mrr then current_mrr - prior_mrr else 0 end as expansion_mrr,
                    case when prior_mrr > 0 and current_mrr < prior_mrr and current_mrr > 0 then prior_mrr - current_mrr else 0 end as contraction_mrr,
                    case when prior_mrr > 0 and current_mrr = 0 then prior_mrr else 0 end as churn_mrr
                from account_monthly_mrr
            ),
            monthly as (
                select
                    snapshot_month,
                    sum(prior_mrr) as starting_mrr,
                    sum(new_mrr) as new_mrr,
                    sum(expansion_mrr) as expansion_mrr,
                    sum(contraction_mrr) as contraction_mrr,
                    sum(churn_mrr) as churn_mrr,
                    sum(current_mrr) as ending_mrr
                from classified
                group by snapshot_month
            )
            select count(*)
            from monthly
            where round(starting_mrr + new_mrr + expansion_mrr - contraction_mrr - churn_mrr, 4) != round(ending_mrr, 4)
            """
        ).fetchone()[0]
        checks["higher"] = f"Months violating MRR bridge equation: {movement_mismatches}"
    finally:
        higher_conn.close()

    return checks


def main() -> int:
    cases = [
        {
            "name": "lower/q001_conversion_funnel_basics",
            "database": REPO_ROOT / "data" / "duckdb" / "q001_lower.duckdb",
            "sql": REPO_ROOT / "solutions" / "lower" / "q001_conversion_funnel_basics.sql",
        },
        {
            "name": "core/q001_monthly_revenue_trends",
            "database": REPO_ROOT / "data" / "duckdb" / "q001_core.duckdb",
            "sql": REPO_ROOT / "solutions" / "core" / "q001_monthly_revenue_trends.sql",
        },
        {
            "name": "core/q002_channel_customer_mix",
            "database": REPO_ROOT / "data" / "duckdb" / "q002_core.duckdb",
            "sql": REPO_ROOT / "solutions" / "core" / "q002_channel_customer_mix.sql",
        },
        {
            "name": "higher/q001_subscription_mrr_movements",
            "database": REPO_ROOT / "data" / "duckdb" / "q001_higher.duckdb",
            "sql": REPO_ROOT / "solutions" / "higher" / "q001_subscription_mrr_movements.sql",
        },
    ]

    report_lines = [
        "# Solution Validation Log",
        "",
        f"- Generated at: {datetime.now(timezone.utc).isoformat()}",
        "- Scope: execute each reference solution statement against its bucket-specific DuckDB file.",
        "- Assumption (lower): milestone events counted once per user using `max(case ...)` flags.",
        "- Assumption (core): rolling average uses available history for early months (fewer than 3 rows).",
        "- Assumption (core q002): prior-month channel revenue defaults to `0` when missing for MoM delta.",
        "- Assumption (higher): missing prior month mrr is treated as `0` via `lag(..., default 0)` logic.",
        "",
    ]

    for case in cases:
        report_lines.append(f"## {case['name']}")
        report_lines.append("")
        report_lines.append(f"- Database: `{case['database'].relative_to(REPO_ROOT)}`")
        report_lines.append(f"- SQL file: `{case['sql'].relative_to(REPO_ROOT)}`")
        report_lines.append("")
        execution_results = _run_solution(case["database"], case["sql"])
        for result in execution_results:
            report_lines.append(
                f"- Statement {result['statement_number']}: `{result['row_count']}` rows"
            )
            report_lines.append("")
            report_lines.append("```text")
            report_lines.append(result["preview"])
            report_lines.append("```")
            report_lines.append("")

    checks = _run_invariant_checks()
    report_lines.append("## Invariant Checks")
    report_lines.append("")
    report_lines.append(f"- Core: {checks['core']}")
    report_lines.append(f"- Lower: {checks['lower']}")
    report_lines.append(f"- Higher: {checks['higher']}")
    report_lines.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
