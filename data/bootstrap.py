"""
Build DuckDB files for every question that has a generator.

From repo root:
  python data/bootstrap.py           # all questions
  python data/bootstrap.py q001      # one question
  python data/bootstrap.py q001 ...  # selected questions

Convention for new questions: add data/generators/generate_q*.py that writes
data/duckdb/<schema_id>.duckdb
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

DUCKDB_DIR_NAME = "duckdb"


def _duckdb_dir(data_dir: Path) -> Path:
    return data_dir / DUCKDB_DIR_NAME


def _question_db_path(data_dir: Path, qid: str) -> Path:
    """Prefer data/duckdb/qNNN.duckdb; fall back to legacy data/qNNN.duckdb."""
    preferred = _duckdb_dir(data_dir) / f"{qid}.duckdb"
    if preferred.exists():
        return preferred
    legacy = data_dir / f"{qid}.duckdb"
    return legacy if legacy.exists() else preferred


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

    # Attach only a single, non-interactive snapshot for editing/queries.
    # Per-question .duckdb files may be locked by Cursor; schema switching
    # happens inside the workspace snapshot instead.
    databases = [
        {
            "alias": "workspace",
            "type": "file",
            "path": "data/duckdb/workspace_build.duckdb",
            "readOnly": True,
            "attached": False,
        }
    ]
    existing["duckdb.databases"] = databases
    existing["duckdb.defaultDatabase"] = "workspace"

    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4)
        f.write("\n")


def _sync_scratchpad_workspace_path(root_dir: Path, workspace_path: Path) -> None:
    scratchpad_path = root_dir / "scratchpad.sql"
    if not scratchpad_path.exists():
        return

    lines = scratchpad_path.read_text(encoding="utf-8").splitlines()
    try:
        workspace_display_path = workspace_path.relative_to(root_dir).as_posix()
    except ValueError:
        workspace_display_path = workspace_path.as_posix()
    target_line = f"attach '{workspace_display_path}' as workspace_db;"
    updated_lines: list[str] = []
    replaced = False

    for line in lines:
        stripped = line.strip().lower()
        if (
            not stripped.startswith("--")
            and "attach '" in stripped
            and "' as workspace_db;" in stripped
        ):
            updated_lines.append(target_line)
            replaced = True
        else:
            updated_lines.append(line)

    if not replaced:
        return

    scratchpad_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def _qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _build_workspace_db(data_dir: Path, question_ids: list[str]) -> tuple[list[str], Path]:
    import duckdb

    skipped: list[str] = []
    duckdb_dir = _duckdb_dir(data_dir)
    duckdb_dir.mkdir(parents=True, exist_ok=True)
    workspace_path = duckdb_dir / "workspace_build.duckdb"
    fallback_workspace_path = duckdb_dir / "workspace_build_pending.duckdb"

    if workspace_path.exists():
        try:
            workspace_path.unlink()
        except OSError as exc:
            if not _file_in_use_error(exc):
                raise
            workspace_path = fallback_workspace_path
            if workspace_path.exists():
                try:
                    workspace_path.unlink()
                except OSError:
                    pass
            print(
                "Could not replace data/duckdb/workspace_build.duckdb because it is still open "
                "(often from an active SQL tab). Building into "
                "data/duckdb/workspace_build_pending.duckdb for this run.",
                file=sys.stderr,
            )

    conn = duckdb.connect(str(workspace_path))
    try:
        for qid in question_ids:
            source_path = _question_db_path(data_dir, qid)
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

    return skipped, workspace_path


def _file_in_use_error(exc: OSError) -> bool:
    winerror = getattr(exc, "winerror", None)
    if winerror == 32:
        return True
    errno = getattr(exc, "errno", None)
    if errno in (11, 13, 16):  # EAGAIN, EACCES, EBUSY (platform-dependent)
        return True
    lowered = str(exc).lower()
    return "being used by another process" in lowered or "text file busy" in lowered


def _refresh_verification_db(data_dir: Path, workspace_path: Path) -> None:
    duckdb_dir = _duckdb_dir(data_dir)
    verification_path = duckdb_dir / "workspace_verify.duckdb"
    if not workspace_path.exists():
        return

    if verification_path.exists():
        try:
            verification_path.unlink()
        except OSError as exc:
            if not _file_in_use_error(exc):
                raise
            pending = duckdb_dir / "workspace_verify_pending.duckdb"
            try:
                if pending.exists():
                    pending.unlink()
            except OSError:
                pass
            shutil.copy2(workspace_path, pending)
            print(
                "Could not replace data/duckdb/workspace_verify.duckdb because another program "
                "still has it open (often the DuckDB view in the editor). "
                f"Wrote the fresh snapshot as data/duckdb/{pending.name} instead. "
                "Close that database in the UI (or reload the window), delete or rename the old "
                "workspace_verify.duckdb if needed, then rerun bootstrap—or rename the pending "
                "file to workspace_verify.duckdb when nothing is using the old file.",
                file=sys.stderr,
            )
            return

    shutil.copy2(workspace_path, verification_path)


def main() -> int:
    if importlib.util.find_spec("duckdb") is None:
        print("duckdb is not installed for this Python interpreter.", file=sys.stderr)
        print(f'  "{sys.executable}" -m pip install -r requirements.txt', file=sys.stderr)
        return 1

    data_dir = Path(__file__).resolve().parent
    _duckdb_dir(data_dir).mkdir(parents=True, exist_ok=True)
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
    workspace_skipped, workspace_path = _build_workspace_db(data_dir, all_ids)
    _refresh_verification_db(data_dir, workspace_path)
    _sync_duckdb_workspace_settings(data_dir.parent, all_ids)
    _sync_scratchpad_workspace_path(data_dir.parent, workspace_path)

    workspace_hint_path = _duckdb_dir(data_dir) / "workspace_last_build.txt"
    workspace_hint_path.write_text(
        str(workspace_path.relative_to(data_dir.parent)),
        encoding="utf-8",
    )
    print(f"Workspace build file for this run: {workspace_path.relative_to(data_dir.parent)}")

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

    if workspace_path.name != "workspace_build.duckdb":
        print(
            "scratchpad.sql was auto-updated to the newest workspace file for this run. "
            "Re-run scratchpad to pick up the new attachment.",
            file=sys.stderr,
        )

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
