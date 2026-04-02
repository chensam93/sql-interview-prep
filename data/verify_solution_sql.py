"""
Validate a solution SQL file against a local DuckDB.

Default database is data/duckdb/workspace_verify.duckdb (bootstrap snapshot).
Falls back to legacy paths if present.

Examples:
  python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql
  python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Validate SQL file with DuckDB.")
    parser.add_argument("--sql", required=True, help="Path to SQL file to execute.")
    parser.add_argument(
        "--database",
        default=str(repo_root / "data" / "duckdb" / "workspace_verify.duckdb"),
        help="DuckDB file to run against (default: data/duckdb/workspace_verify.duckdb).",
    )
    parser.add_argument(
        "--schema",
        default=None,
        help="Optional schema to set before executing (for example: q001).",
    )
    args = parser.parse_args()

    sql_path = Path(args.sql)
    if not sql_path.is_absolute():
        sql_path = (repo_root / sql_path).resolve()
    if not sql_path.exists():
        print(f"SQL file not found: {sql_path}", file=sys.stderr)
        return 1

    database_path = Path(args.database)
    if not database_path.is_absolute():
        database_path = (repo_root / database_path).resolve()
    if not database_path.exists():
        for fallback in (
            repo_root / "data" / "workspace_verify.duckdb",
            repo_root / "data" / "workspace.duckdb",
        ):
            if fallback.exists():
                database_path = fallback
                break
        else:
            print(f"Database file not found: {args.database}", file=sys.stderr)
            return 1

    sql_text = sql_path.read_text(encoding="utf-8")

    try:
        connection = duckdb.connect(str(database_path), read_only=True)
    except Exception as exc:
        print(f"Could not open database {database_path}: {exc}", file=sys.stderr)
        return 1

    try:
        if args.schema:
            connection.execute(f"set schema = '{args.schema}'")
        connection.execute(sql_text)
    except Exception as exc:
        print(f"SQL validation failed: {exc}", file=sys.stderr)
        return 1
    finally:
        connection.close()

    print(f"SQL validation succeeded: {sql_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
