# SQL Interview Prep

A live, queryable SQL practice environment for senior analytics engineering interviews.

## How it works

1. Pick a question from `questions/`
2. Build local DuckDB files with `python data/bootstrap.py` (see **Data** below)
3. Query `data/workspace.duckdb` (default in workspace settings); each question lives in its own schema like `q001`
4. Write your answer in `scratchpad.sql` (gitignored — your private workspace)
5. Review the reference solution in `solutions/` when ready

## Setup

Requires Python 3.9+:

```bash
pip install -r requirements.txt
```

## Data

`*.duckdb` files are gitignored (regenerate locally). One command builds **every** question that has a `data/generators/generate_qNNN.py` script and also creates `data/workspace.duckdb`:

```bash
python data/bootstrap.py
```

Build specific questions only:

```bash
python data/bootstrap.py q001
```

**Adding a new question:** add `questions/qNNN_….md`, `data/generators/generate_qNNN.py` (writing `data/qNNN.duckdb`), and `solutions/…`. The next `bootstrap.py` run picks up the new generator automatically.

**Cursor / VS Code:** **Terminal → Run Build Task** (or `Ctrl+Shift+B` / `Cmd+Shift+B`) runs `python data/bootstrap.py` as the default build task.

`bootstrap.py` also syncs `.vscode/settings.json` so DuckDB Explorer defaults to `workspace.duckdb`. Switch questions by changing schema, e.g. `SET schema = 'q001';` or by querying `q001.users`, `q001.activity`, etc.

`bootstrap.py` also refreshes `data/workspace_verify.duckdb`, a validation snapshot used for non-interactive SQL checks.

To rebuild automatically when you open this folder, add `"runOptions": { "runOn": "folderOpen" }` to that task in `.vscode/tasks.json` (fine for small datasets; skip if generation gets slow).

(You can `pip install duckdb` directly instead of `requirements.txt` if you prefer.)

### Directory layout

- `data/generators/` - question-specific data builders (`generate_qNNN.py`)
- `data/qNNN.duckdb` - per-question DuckDB files produced by generators
- `data/workspace.duckdb` - combined database with one schema per question (`q001`, `q002`, ...)
- `data/workspace_verify.duckdb` - validation snapshot for automated SQL verification

### Validate solutions

```bash
python data/verify_solution_sql.py --sql solutions/q001_cohort_retention.sql --schema q001
```

## Questions

| # | Topic | Concepts tested |
|---|-------|-----------------|
| [Q001](questions/q001_cohort_retention.md) | Cohort Retention | window functions, date math, self-join vs window, cohort bucketing |
| [Q002](questions/q002_monthly_revenue_trends.md) | Monthly Revenue Trends | aggregation, rolling window average, ranking |

## Philosophy

Questions mirror real senior AE interview scenarios:
- Ambiguous requirements that need clarification
- Business logic nuance, not just syntax
- Multiple valid approaches with trade-offs worth discussing
