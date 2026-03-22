# SQL Interview Prep

A live, queryable SQL practice environment for senior analytics engineering interviews.

## How it works

1. Pick a question from `questions/`
2. Run the matching data generation script in `data/` to create a fresh DuckDB file
3. Connect Cursor's DuckDB extension to `data/<question>.duckdb`
4. Write your answer in `scratch.sql` (gitignored — your private workspace)
5. Review the reference solution in `solutions/` when ready

## Setup

Requires Python 3.9+ and duckdb:

```bash
pip install duckdb
```

## Questions

| # | Topic | Concepts tested |
|---|-------|-----------------|
| [Q001](questions/q001_cohort_retention.md) | Cohort Retention | window functions, date math, self-join vs window, cohort bucketing |

## Philosophy

Questions mirror real senior AE interview scenarios:
- Ambiguous requirements that need clarification
- Business logic nuance, not just syntax
- Multiple valid approaches with trade-offs worth discussing
