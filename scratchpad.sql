-- Session bootstrap (run once in a fresh SQL tab/session).
-- This makes scratchpad self-contained even if DuckDB Explorer is on a different DB.
ATTACH 'data/duckdb/workspace_verify.duckdb' AS workspace_db;

-- Quick sanity checks
-- Switch questions by changing EXACTLY ONE line below:
-- Lower Q001:
-- USE workspace_db.q001_lower;
-- Core Q001:
USE workspace_db.q001_core;
-- Higher Q001:
-- USE workspace_db.q001_higher;

SELECT current_database(), current_schema();
SHOW TABLES;

-- Start your answer below
-- SELECT ...
