# SQL Interview Prep

Much of this repository was built with coding-agent assistance (for example Cursor). It is a personal practice scaffold, not production software—review SQL, Python, and data logic before relying on it.

**Development model:** wiring and automation skew AI-assisted; question intent and modeling skew human-led.

Personal scaffold for **SQL practice against real synthetic data**, not static “write SQL, hope it’s right” drills.

The intended workflow is **Cursor (or any similar coding agent)**: you iterate on prompts in `questions/`, adjust generators in `data/generators/`, and run queries in DuckDB so you can **curate your own interview-style questions** and **verify answers against generated tables**.

## Quickstart

```bash
pip install -r requirements.txt
python data/bootstrap.py
```

Open `scratchpad.sql`, attach the workspace DB, then `use workspace_db.<schema_id>;` (for example `workspace_db.q003_core`) and run against the loaded data. Compare with `solutions/` when you want a reference.

Validate a solution file:

```bash
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
```

## Repo layout (short)

| Path | Purpose |
|------|---------|
| `questions/` | Prompts (markdown) |
| `solutions/` | Reference SQL |
| `data/generators/` | Per-question synthetic data builders |
| `data/duckdb/` | Generated `.duckdb` files (gitignored); `workspace_build*.duckdb` merges schemas for scratchpad use |

If `workspace_build.duckdb` is locked (common on Windows), bootstrap may write `workspace_build_pending.duckdb`—attach that for querying.

**VS Code / Cursor:** `.vscode/settings.json` points DuckDB Explorer at `data/duckdb/workspace_verify.duckdb`; **Run Build Task** (`Ctrl+Shift+B`) runs bootstrap.

**Snapshot:** 2026-04-27 — practice scaffold; revise when the repo’s purpose or layout changes materially.

## Secret scanning

Local hook: `git config core.hooksPath .githooks`. CI: `.github/workflows/secret-scan.yml`, config `.gitleaks.toml`.
