# SQL Interview Prep

A live, queryable SQL practice environment for analytics engineering interviews (personal project).
I wanted to practice my SQL for analytic engineer technical interviews but I didn't want to rely on Leetcode or similar websites. I just wanted to use Cursor and adjust the questions/parameters myself. It's easy to curate questions oneself via an LLM but I wanted data to actually query, not simply respond with SQL that I can't manually verify.

## Practice-Only Disclaimer
This repo is my SQL interview practice scaffolding. It is not intended as a public package, production system, or reference implementation for others to consume.

Expect incomplete/iterating code; review any SQL/Python before relying on it.

## Note on AI assistance
Vast majority of code was produced with **Cursor’s Agent**. My best-effort estimate:

- Repo wiring & “how to run” glue (VS Code/Cursor config, `data/bootstrap.py`, per-question generators, verify script, scratchpad wiring): ~70–90% AI-assisted.
- Interview content (the question markdown prompts + question-specific solution SQL in `solutions/`): ~20–40% AI-assisted (mostly for SQL shape/debugging), with the core modeling/intent mostly coming from me.

This is very much **vibe-coded**—treat it as a practice scaffold/draft, not a polished library. Review any generated code before relying on it.

## How it works

1. Pick a question from `questions/`
2. Run `python data/bootstrap.py` (writes per-question DBs under `data/duckdb/` and refreshes `data/duckdb/workspace_verify.duckdb`)
3. Open `scratchpad.sql`, switch to your target schema (for example `use workspace_db.q003_lower;`), and run statements in DuckDB
4. Review `solutions/` when ready

## Config notes (requirements + editor)
- Requirements: `python 3.9+` and `pip install -r requirements.txt`.
- Editor integration: `.vscode/settings.json` points DuckDB Explorer at `data/duckdb/workspace_verify.duckdb` for data inspection.
- Build tasks: `.vscode/tasks.json` defines `SQL Prep: Bootstrap data`.
- Windows: DuckDB files can be locked; if you have a `data/duckdb/qNNN.duckdb` open in Cursor, bootstrap may skip that question until you detach it (rerun bootstrap after closing).

## Setup

Python 3.9+:

```bash
pip install -r requirements.txt
```

## New User Quickstart

For a fresh clone, do this once:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run bootstrap:

```bash
python data/bootstrap.py
```

3. Open `scratchpad.sql`, switch to desired schema (`use workspace_db.q001_lower;`, `use workspace_db.q003_core;`, etc.), and run.

## Secret scanning

- local pre-commit hook lives at `.githooks/pre-commit`
- CI scan runs in `.github/workflows/secret-scan.yml`
- gitleaks config lives at `.gitleaks.toml`

One-time local setup in this repo:

```bash
git config core.hooksPath .githooks
```

Optional (better local detection): install `gitleaks` so the hook runs `gitleaks protect --staged` instead of fallback regex scanning.

## Data

`*.duckdb` files are gitignored. One command runs every `data/generators/generate_q*.py` and refreshes DuckDB workspace files:

```bash
python data/bootstrap.py
```

### What the DuckDB files are

| File | Role |
|------|------|
| `data/duckdb/q001_core.duckdb`, `q001_lower.duckdb`, … | **Source** DB for each question (what generators build). Tables live in schema `main`. |
| `data/duckdb/workspace_build.duckdb` | Merged workspace used for scratchpad querying. |
| `data/duckdb/workspace_verify.duckdb` | Read-only snapshot copy for editor integrations that expect a stable file path. |

When `workspace_build.duckdb` is locked (common on Windows with an attached SQL tab), bootstrap writes `workspace_build_pending.duckdb`.

**Adding a question:** add files under bucketed folders in `questions/` and `solutions/`, plus `data/generators/generate_q...py` that writes `data/duckdb/<schema_id>.duckdb`. Re-run bootstrap.

**Build task:** **Terminal → Run Build Task** (`Ctrl+Shift+B`) runs `SQL Prep: Bootstrap data`.

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/<bucket>/<question_solution>.sql --schema <schema_id>
```

Examples:

```bash
python data/verify_solution_sql.py --sql solutions/lower/q001_conversion_funnel_basics.sql --schema q001_lower
python data/verify_solution_sql.py --sql solutions/lower/q002_resolution_rate_by_channel.sql --schema q002_lower
python data/verify_solution_sql.py --sql solutions/lower/q003_priority_mix_by_channel.sql --schema q003_lower
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
python data/verify_solution_sql.py --sql solutions/core/q002_channel_customer_mix.sql --schema q002_core
python data/verify_solution_sql.py --sql solutions/core/q003_monthly_net_after_returns.sql --schema q003_core
python data/verify_solution_sql.py --sql solutions/higher/q001_subscription_mrr_movements.sql --schema q001_higher
```

### Layout

| Path | Role |
|------|------|
| `scratchpad.sql` | DuckDB scratchpad template |
| `data/generators/` | Dataset scripts |
| `data/duckdb/` | All `.duckdb` artifacts (per-question + workspace snapshots) |
| `data/verify_solution_sql.py` | Non-interactive SQL check |

## Questions

| # | Difficulty bucket | Topic | Concepts tested |
|---|-------------------|-------|-----------------|
| [Q001](questions/lower/q001_conversion_funnel_basics.md) | lower | Weekly Ticket Resolution Basics | left join filtering, count distinct, date bucketing, case statements |
| [Q002](questions/lower/q002_resolution_rate_by_channel.md) | lower | 7-Day Resolution Rate by Channel | left join, case statements, grouped aggregation |
| [Q003](questions/lower/q003_priority_mix_by_channel.md) | lower | Priority Mix by Channel | conditional aggregation, grouped counts, case statements |
| [Q001](questions/core/q001_monthly_revenue_trends.md) | core (mid + senior blend) | Monthly Revenue Trends | aggregation, rolling average, ranking |
| [Q002](questions/core/q002_channel_customer_mix.md) | core (mid + senior blend) | Channel Revenue Mix (New vs Returning) | ctes, window functions, conditional aggregation, ranking |
| [Q003](questions/core/q003_monthly_net_after_returns.md) | core (mid + senior blend) | Monthly gross vs refunds | ctes, joins, aggregation, coalesce, null-safe ratios |
| [Q001](questions/higher/q001_subscription_mrr_movements.md) | higher | Subscription MRR Movements | ctes, window functions, lifecycle classification |


