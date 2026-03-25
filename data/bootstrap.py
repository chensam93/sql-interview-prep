"""
Build DuckDB files for every question that has a generator.

From repo root:
  python data/bootstrap.py           # all questions
  python data/bootstrap.py q001      # one question
  python data/bootstrap.py q001 q002 # several

Convention for new questions: add data/generators/generate_qNNN.py that writes
data/qNNN.duckdb
(this repo’s pattern). Re-run this script after pulling new generators.
"""

from __future__ import annotations

import argparse
import shutil
import importlib.util
import json
import runpy
import sys
from pathlib import Path


def _generators(data_dir: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    generators_dir = data_dir / "generators"
    for path in sorted(generators_dir.glob("generate_q*.py")):
        stem = path.stem  # generate_q001
        if not stem.startswith("generate_q") or len(stem) <= len("generate_q"):
            continue
        qid = stem[len("generate_") :]  # q001
        out[qid] = path
    return out


def _sync_duckdb_workspace_settings(root_dir: Path, question_ids: list[str]) -> None:
    settings_path = root_dir / ".vscode" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict[str, object] = {}
    if settings_path.exists():
        with settings_path.open("r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                print(
                    f"Warning: could not parse {settings_path}; skipping DuckDB settings sync.",
                    file=sys.stderr,
                )
                return

    databases = [
        {
            "alias": "workspace",
            "type": "file",
            "path": "${workspaceFolder}/data/workspace.duckdb",
            "readOnly": False,
            "attached": True,
        }
    ] + [
        {
            "alias": qid,
            "type": "file",
            "path": f"${{workspaceFolder}}/data/{qid}.duckdb",
            "readOnly": False,
            "attached": True,
        }
        for qid in question_ids
    ]
    existing["duckdb.databases"] = databases
    existing["duckdb.defaultDatabase"] = "workspace"

    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)
        f.write("\n")


def _qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _build_workspace_db(data_dir: Path, question_ids: list[str]) -> list[str]:
    import duckdb

    skipped: list[str] = []
    workspace_path = data_dir / "workspace.duckdb"

    conn = duckdb.connect(str(workspace_path))
    try:
        for qid in question_ids:
            source_path = data_dir / f"{qid}.duckdb"
            if not source_path.exists():
                continue

            src_alias = f"src_{qid}"
            quoted_alias = _qident(src_alias)
            try:
                conn.execute(
                    f"ATTACH '{source_path.as_posix()}' AS {quoted_alias} (READ_ONLY)"
                )
            except (OSError, duckdb.IOException) as exc:
                msg = str(exc).lower()
                if (
                    "already open" in msg
                    or "being used by another process" in msg
                    or "cannot open file" in msg
                ):
                    print(
                        f"  Workspace merge skipped {qid}: file is open elsewhere "
                        f"({source_path.name}). Detach it and rerun bootstrap to include it.",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"  Workspace merge skipped {qid}: {exc}",
                        file=sys.stderr,
                    )
                skipped.append(qid)
                continue
            except Exception as exc:
                print(f"  Workspace merge skipped {qid}: {exc}", file=sys.stderr)
                skipped.append(qid)
                continue

            try:
                conn.execute(f"CREATE SCHEMA IF NOT EXISTS {_qident(qid)}")

                rows = conn.execute(
                    f"SHOW TABLES FROM {quoted_alias}.main"
                ).fetchall()
                for (table_name,) in rows:
                    conn.execute(
                        f"""
                        CREATE OR REPLACE TABLE {_qident(qid)}.{_qident(table_name)} AS
                        SELECT * FROM {quoted_alias}.main.{_qident(table_name)}
                        """
                    )
            finally:
                try:
                    conn.execute(f"DETACH {quoted_alias}")
                except Exception:
                    pass
    finally:
        conn.close()

    return skipped


def _refresh_verification_db(data_dir: Path) -> None:
    workspace_path = data_dir / "workspace.duckdb"
    verification_path = data_dir / "workspace_verify.duckdb"
    shutil.copy2(workspace_path, verification_path)


def main() -> int:
    if importlib.util.find_spec("duckdb") is None:
        print("duckdb is not installed for this Python interpreter.", file=sys.stderr)
        print(f'  "{sys.executable}" -m pip install -r requirements.txt', file=sys.stderr)
        return 1

    data_dir = Path(__file__).resolve().parent
    by_id = _generators(data_dir)
    if not by_id:
        print("No data/generators/generate_q*.py scripts found.", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="Build DuckDB datasets for SQL prep questions.")
    parser.add_argument(
        "questions",
        nargs="*",
        metavar="QID",
        help="Question ids to build (e.g. q001). Default: all.",
    )
    args = parser.parse_args()
    to_run = sorted(by_id.keys()) if not args.questions else args.questions

    unknown = [q for q in to_run if q not in by_id]
    if unknown:
        print(f"Unknown question id(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(by_id.keys()))}", file=sys.stderr)
        return 1

    failed: list[str] = []
    for qid in to_run:
        script = by_id[qid]
        print(f"Running {script.name} ...", flush=True)
        try:
            runpy.run_path(str(script), run_name="__main__")
        except KeyboardInterrupt:
            raise
        except SystemExit as e:
            if e.code not in (0, None):
                failed.append(qid)
        except Exception:
            failed.append(qid)
            msg = str(sys.exc_info()[1])
            if "File is already open" in msg or "being used by another process" in msg:
                print(
                    f"  {qid}: database file is locked by another app/session.",
                    file=sys.stderr,
                )
                print(
                    "  Close/detach that database in DuckDB Explorer, then rerun bootstrap.",
                    file=sys.stderr,
                )
            else:
                print(f"  {qid}: unexpected error while generating data.", file=sys.stderr)
            continue

    all_ids = sorted(by_id.keys())
    workspace_skipped = _build_workspace_db(data_dir, all_ids)
    _refresh_verification_db(data_dir)
    _sync_duckdb_workspace_settings(data_dir.parent, all_ids)

    if workspace_skipped:
        print(
            f"Workspace built without: {', '.join(workspace_skipped)} "
            "(detach those databases in the IDE, then rerun bootstrap).",
            file=sys.stderr,
        )

    if failed:
        print(f"Failed: {', '.join(failed)}", file=sys.stderr)
        print(
            "Workspace was still refreshed from existing qNNN.duckdb files on disk.",
            file=sys.stderr,
        )
        return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
