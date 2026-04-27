# SQL Interview Prep

Much of this repository was built with coding-agent assistance (for example Cursor). It is a personal practice scaffold, not production software—review SQL, Python, and data logic before relying on it.

**What you get:** Interview-style prompts with **real rows in DuckDB**, so you run SQL and inspect results instead of guessing on paper.

**How to use it:** Read a prompt in `questions/` → install deps and run `bootstrap` once per refresh → open the workspace database in `scratchpad.sql`, attach the schema for that question (`use workspace_db.<schema_id>;`) → write and run your query. Peek at `solutions/` or the verify command below when you want a reference. If you use **Cursor or a similar agent**, you can iterate on prompts and regenerate data without leaving the repo.

## Quickstart

```bash
pip install -r requirements.txt
python data/bootstrap.py
```

In `scratchpad.sql`, attach the workspace file under `data/duckdb/` (often `workspace_build.duckdb`; if it is locked on Windows, use `workspace_build_pending.duckdb` instead), then for example:

```sql
use workspace_db.q003_core;
```

**VS Code / Cursor:** DuckDB Explorer is pointed at `data/duckdb/workspace_verify.duckdb` in `.vscode/settings.json`. **Run Build Task** (`Ctrl+Shift+B`) runs bootstrap again.

Optional—check a reference solution against the built data:

```bash
python data/verify_solution_sql.py --sql solutions/core/q001_monthly_revenue_trends.sql --schema q001_core
```

**Development model / snapshot:** Automation skews AI-assisted; question intent skews human-led. README snapshot: 2026-04-27.
