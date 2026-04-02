# SQL Interview Prep

A live, queryable SQL practice environment for senior analytics engineering interviews (personal project).

## Practice-Only Disclaimer
This repo is my SQL interview practice scaffolding. It is not intended as a public package, production system, or reference implementation for others to consume.

Expect incomplete/iterating code; review any SQL/Python before relying on it.

## Note on AI assistance
Some tooling/scaffolding was produced with **Cursor’s Agent**. Treat generated code as a draft and review it.

## How it works

1. Pick a question from `questions/`
2. Run `python data/bootstrap.py` (writes per-question DBs under `data/duckdb/` and refreshes `data/duckdb/workspace_verify.duckdb`)
3. Query via **`data/duckdb/workspace_verify.duckdb`**: each question is a schema (`q001`, `q002`, …). Use **`scratchpad.sql`** (shared template) — attach once, then switch with `USE workspace_db.q00N;` For private notes, use **`personal_scratch.sql`** (gitignored).
4. Review `solutions/` when ready

## Setup

Python 3.9+:

```bash
pip install -r requirements.txt
```

## Data

`*.duckdb` files are gitignored. One command runs every `data/generators/generate_qNNN.py` and merges question DBs into a single practice snapshot:

```bash
python data/bootstrap.py
```

### What the DuckDB files are

| File | Role |
|------|------|
| `data/duckdb/q001.duckdb`, `q002.duckdb`, … | **Source** DB for each question (what generators build). Tables live in schema `main`. |
| `data/duckdb/workspace_build.duckdb` | **Temporary** merge: copies each `qNNN` into its own schema (`q001`, `q002`, …) then feeds the verify file. |
| `data/duckdb/workspace_verify.duckdb` | **What you query in practice** — one file, switch schema to change question. Safe to open while per-question files may be locked. |

If a per-question file is open in Cursor, bootstrap may skip merging that question until you detach it. Bootstrap still looks for **legacy** `data/qNNN.duckdb` if the new path is missing (one-time migration).

**Adding a question:** `questions/…`, `data/generators/generate_qNNN.py` → `data/duckdb/qNNN.duckdb`, `solutions/…`. Re-run bootstrap.

**Build task:** **Terminal → Run Build Task** (`Ctrl+Shift+B`) runs `python data/bootstrap.py`.

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/q002_monthly_revenue_trends.sql --schema q002
```

### Layout

| Path | Role |
|------|------|
| `scratchpad.sql` | Session template (attach + question switch + sanity checks) |
| `data/generators/` | Dataset scripts |
| `data/duckdb/` | All `.duckdb` artifacts (per-question + workspace snapshots) |
| `data/verify_solution_sql.py` | Non-interactive SQL check |

## Questions

| # | Topic | Concepts tested |
|---|-------|-----------------|
| [Q001](questions/q001_cohort_retention.md) | Cohort Retention | windows, dates, cohorts, ratios |
| [Q002](questions/q002_monthly_revenue_trends.md) | Monthly Revenue Trends | aggregation, rolling average, ranking |

## Philosophy

Questions mirror senior AE interviews: ambiguous specs, business nuance, multiple defensible SQL shapes.

