"""Offline preparation and scoring around the pinned BuildArena support test.

This module never launches Besiege, posts input events, or writes into its install.
Synthetic traces and handwritten fixtures are plumbing tests, not research results.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import math
import os
import shutil
import sys
import types
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "baseline" / "BuildArena"
COMMIT = "c3005b90686ea6dae9a69a293e7f6395eae77c9c"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_source() -> None:
    manifest = json.loads((ROOT / "baseline" / "buildarena-source.json").read_text())
    if manifest["commit"] != COMMIT:
        raise ValueError("Unexpected upstream source version")
    for relative, expected in manifest["files_sha256"].items():
        if digest(UPSTREAM / relative) != expected:
            raise ValueError(f"Upstream source changed: {relative}")


def workspace_output(path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError("Outputs must stay inside the research workspace")
    return resolved


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


@contextmanager
def upstream_context(staging: Path):
    """Supply only workspace paths and intercept the original GUI entry point."""
    check_source()
    old_cwd = Path.cwd()
    old_path = sys.path[:]
    missing = object()
    old_modules = {name: sys.modules.get(name, missing)
                   for name in ("config", "simulation.operations")}
    config = types.ModuleType("config")
    config.SavedMachines = str(staging)
    operations = types.ModuleType("simulation.operations")
    captured = []

    def capture_sequence(**kwargs):
        captured.append(kwargs)
        return str(Path(kwargs["output_dir"]) /
                   f"simulation_log_{kwargs['machine_name']}.csv")

    operations.run_simulation_sequence = capture_sequence
    staging.mkdir(parents=True, exist_ok=True)
    sys.modules["config"] = config
    sys.modules["simulation.operations"] = operations
    sys.path.insert(0, str(UPSTREAM))
    os.chdir(UPSTREAM)  # Upstream loads block configuration by relative path.
    try:
        yield captured
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
        for name, previous in old_modules.items():
            if previous is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = previous


def prepare(output: Path, machine_json: Path | None = None) -> dict:
    """Run original Support Lv.1 preprocessing while replacing GUI with capture."""
    output = workspace_output(output)
    if output.exists():
        raise ValueError("Use a new output directory to preserve prior artifacts")
    if machine_json is not None:
        machine_json = machine_json.resolve()
        history = json.loads(machine_json.read_text())
        # The upstream replay ignores unknown operations; reject these up front.
        allowed = {"start", "attach_block_to", "connect_blocks", "remove_block",
                   "twist_block", "shift_block", "rotate_block"}
        if not isinstance(history, list) or not history:
            raise ValueError("Expected a nonempty BuildArena operation-history list")
        if any(not isinstance(op, dict) or op.get("op") not in allowed
               or not isinstance(op.get("params"), dict) for op in history):
            raise ValueError("Unsupported or malformed machine operation")
        if history[0]["op"] != "start":
            raise ValueError("Machine history must start with initialization")
    output.mkdir(parents=True)
    staging = output / "game-staging"
    task = output / "support_soft_plumbing_20261013_000000"
    machine_dir = task / "machine" / "research_bridge_fixture"
    machine_dir.mkdir(parents=True)
    source_json = machine_dir / "research_bridge_fixture.json"

    with upstream_context(staging) as captured:
        if machine_json is None:
            from spatial.build import Machine

            fixture = Machine(name="research_bridge_fixture", save_dir=str(machine_dir),
                              db_path=str(task / "task_database.db"))
            fixture.start(note="Handwritten short-span plumbing fixture; not LLM output")
            for _ in range(3):
                base = max(fixture.blocks, key=int)
                faces = fixture.blocks[base].faces
                # Pick the exposed face pointing along the game z axis.
                face = next(key for key, value in faces.items()
                            if value.sticky and value.normal.vec_abs.virtual[2] > 0.9)
                fixture.attach_block_to(base, face, "Small Wooden Block",
                                        note="plumbing fixture")
            if len(fixture.blocks) != 4:
                raise RuntimeError("Fixture construction did not produce four blocks")
            fixture.to_file(str(machine_dir))
        else:
            shutil.copyfile(machine_json, source_json)

        support = importlib.import_module("simulation.simulation_support")
        support = importlib.reload(support)  # Bind this run's workspace staging path.
        expected_csv = support.main(str(source_json), "soft")
        if len(captured) != 1:
            raise RuntimeError("Expected exactly one intercepted simulation request")

    level = staging / "research_support_soft.blv"
    shutil.copyfile(UPSTREAM / "asset" / "support_soft.blv", level)
    bsg = staging / "research_bridge_fixture_sim.bsg"
    result = {
        "status": "prepared_offline", "upstream_commit": COMMIT,
        "fixture_kind": "handwritten_plumbing_only" if machine_json is None else "supplied_history",
        "simulation_executed": False, "level": "soft", "duration_seconds": 17,
        "machine_bsg": str(bsg), "custom_level": str(level),
        "expected_csv": expected_csv, "captured_request": captured[0],
        "artifact_sha256": {str(p.relative_to(output)): digest(p)
                            for p in (bsg, level, source_json)},
    }
    write_json(output / "preparation.json", result)
    return result


def analyze(csv_path: Path, output: Path) -> dict:
    """Validate log completeness, then reuse original support scoring unchanged."""
    csv_path = csv_path.resolve()
    output = workspace_output(output)
    if output == csv_path or output.with_suffix(".clean.csv") == csv_path:
        raise ValueError("Do not overwrite the source telemetry")
    check_source()
    records = {}
    with csv_path.open(newline="") as stream:
        for number, row in enumerate(csv.reader(stream), 1):
            if len(row) < 2 or row[1].strip() != "ID_Ballast":
                continue
            row = [value.strip() for value in row]
            while row and row[-1] == "":
                row.pop()
            if len(row) not in (3, 5):
                raise ValueError(f"Malformed ballast record at line {number}")
            values = [float(row[0]), *map(float, row[2:])]
            if not all(math.isfinite(value) for value in values) or values[0] < 0:
                raise ValueError(f"Invalid numeric telemetry at line {number}")
            if len(row) == 3 and values[1] < 0:
                raise ValueError("Negative ballast mass")
            key = (values[0], len(row))
            numeric_row = (values[0], "ID_Ballast", *values[1:])
            if key in records and records[key] != numeric_row:
                raise ValueError(f"Conflicting ballast samples at time {values[0]}")
            records[key] = numeric_row
    positions = [row for (_, length), row in records.items() if length == 5]
    weights = [row for (_, length), row in records.items() if length == 3]
    if len(positions) < 2 or not weights:
        raise ValueError("Incomplete ballast telemetry: need position and mass samples")
    position_times = {row[0] for row in positions}
    weight_times = {row[0] for row in weights}
    if position_times != weight_times:
        raise ValueError("Position and mass timestamps do not match")
    clean = output.with_suffix(".clean.csv")
    clean.parent.mkdir(parents=True, exist_ok=True)
    # Position-first ordering prevents ragged pandas inference from dropping positions.
    rows = sorted(records.values(), key=lambda row: (row[0], -len(row)))
    with clean.open("w", newline="") as stream:
        csv.writer(stream).writerows(rows)
    with upstream_context(output.parent / "unused-game-staging"):
        scorer = importlib.import_module("analyze.sim_support")
        stats = scorer._analyze_ballast_support(str(clean))
        passed = bool(stats["hold_time_above_threshold"] >= scorer.HOLD_THRESHOLD
                      and not stats["initial_height_above_threshold"])
    result = {
        "status": "scored", "upstream_commit": COMMIT, "legacy_pass": passed,
        "input_csv": str(csv_path), "input_sha256": digest(csv_path),
        "position_samples": len(positions), "mass_samples": len(weights),
        "metrics": stats,
        "meaning": "Original BuildArena score; not a sustained fixed-load certificate",
    }
    write_json(output, result)
    return result


def doctor() -> dict:
    steam = Path.home() / "Library/Application Support/Steam/steamapps"
    app = steam / "common/Besiege/Besiege.app/Contents"
    mod = steam / "workshop/content/346010/2383785201/LuaScripting"
    check_source()
    return {
        "python": sys.version.split()[0], "upstream_commit": COMMIT,
        "source_integrity": "verified",
        "besiege_at_default_location": app.is_dir(),
        "lua_mod_files_present": (mod / "Mod.xml").is_file() and (mod / "Main.dll").is_file(),
        "live_mod_activation_verified": False, "live_simulation_verified": False,
        "original_test": {"level": "soft", "gap_units": 5, "duration_seconds": 17,
                          "height_threshold": 4, "accumulated_hold_seconds": 2},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    status = sub.add_parser("doctor")
    status.add_argument("--output", type=Path)
    prep = sub.add_parser("prepare")
    prep.add_argument("--out-dir", type=Path, required=True)
    prep.add_argument("--machine-json", type=Path)
    score = sub.add_parser("analyze")
    score.add_argument("--csv", type=Path, required=True)
    score.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            result = doctor()
            if args.output:
                write_json(workspace_output(args.output), result)
        elif args.command == "prepare":
            result = prepare(args.out_dir, args.machine_json)
        else:
            result = analyze(args.csv, args.output)
    except (ValueError, OSError, ImportError, RuntimeError) as exc:
        print(json.dumps({"status": "infrastructure_error", "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
