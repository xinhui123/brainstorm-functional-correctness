"""Save repeated manual copies of Besiege's rolling log on macOS.

Reads the clipboard only while this command runs, retains only numeric
ID_Ballast records, and never sends game input or changes the simulation.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import subprocess
import time
from datetime import datetime
from itertools import pairwise
from pathlib import Path

from bridge_harness import ROOT, analyze, workspace_output, write_json


def ballast_rows(text: str) -> list[tuple]:
    rows = []
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 2 or row[1].strip() != "ID_Ballast":
            continue
        if len(row) not in (3, 5):
            raise ValueError("Malformed ballast clipboard record")
        values = [float(row[0]), *map(float, row[2:])]
        if not all(math.isfinite(x) for x in values) or values[0] < 0:
            raise ValueError("Invalid numeric ballast clipboard record")
        if len(row) == 3 and values[1] < 0:
            raise ValueError("Negative ballast mass")
        rows.append((values[0], "ID_Ballast", *values[1:]))
    return rows


class Capture:
    def __init__(self):
        self.records: set[tuple] = set()
        self.latest = 0.0
        self.snapshots = 0

    def add(self, rows: list[tuple]) -> bool:
        if not rows:
            return False
        first, last = min(r[0] for r in rows), max(r[0] for r in rows)
        if not self.records and first > 0.12:
            return False  # A late tail cannot initialize a complete run.
        if self.records and last < self.latest - 0.12:
            raise ValueError("Simulation clock restarted; use a new recorder for each run")
        before = len(self.records)
        self.records.update(rows)
        self.latest = max(self.latest, last)
        if len(self.records) == before:
            return False
        self.snapshots += 1
        return True

    def summary(self) -> dict:
        positions = [r for r in self.records if len(r) == 5]
        masses = [r for r in self.records if len(r) == 3]
        pt, mt = {r[0] for r in positions}, {r[0] for r in masses}
        times = sorted(pt)
        first = times[0] if times else None
        last = times[-1] if times else None
        gap = max((b - a for a, b in pairwise(times)), default=0.0)
        complete = bool(
            times and first <= 0.12 and last >= 17.0
            and gap <= 0.120001 and pt == mt
            and any(r[0] >= 17.0 and abs(r[2] - 1500) < 0.01 for r in masses)
        )
        return {
            "position_samples": len(positions), "mass_samples": len(masses),
            "first_time": first, "last_time": last, "largest_gap": gap,
            "position_without_mass": sorted(pt - mt),
            "mass_without_position": sorted(mt - pt),
            "snapshots": self.snapshots, "complete_load_window": complete,
        }


def read_clipboard() -> str:
    return subprocess.run(
        ["/usr/bin/pbpaste"], capture_output=True, text=True, check=True, timeout=3,
    ).stdout


def record(output: Path, timeout: float) -> int:
    output = workspace_output(output)
    output.mkdir(parents=True, exist_ok=False)
    capture = Capture()
    previous = read_clipboard()  # Ignore the clipboard already present when armed.
    deadline = time.monotonic() + timeout
    print("READY: reload the fixture and start a fresh run at 100% speed.", flush=True)
    print("Click the black Log panel; press Command+A then Command+C every 2-3 seconds.",
          flush=True)
    print("Do not switch to chat or restart the run. After 17 seconds, stop and copy once more.",
          flush=True)
    try:
        while time.monotonic() < deadline:
            text = read_clipboard()
            if text != previous:
                previous = text
                rows = ballast_rows(text)
                if capture.add(rows):
                    # Save only the requested telemetry, never unrelated clipboard text.
                    target = output / f"snapshot-{capture.snapshots:03d}.csv"
                    with target.open("w", newline="") as stream:
                        csv.writer(stream).writerows(rows)
                    with (output / "ballast-captures.csv").open("a", newline="") as stream:
                        csv.writer(stream).writerows(rows)
                    summary = capture.summary()
                    write_json(output / "capture-summary.json", summary)
                    print(f"Saved through {summary['last_time']:.2f}s "
                          f"({summary['position_samples']} position samples).", flush=True)
                    if summary["complete_load_window"]:
                        analyze(output / "ballast-captures.csv", output / "legacy-score.json")
                        print(f"CAPTURE COMPLETE. Stop Besiege now. Results: {output}", flush=True)
                        return 0
                elif rows and not capture.records:
                    print("Waiting for a new run's early log; first copy must be before 6 seconds.",
                          flush=True)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("Capture stopped; retained copies are preserved.", flush=True)
    summary = capture.summary()
    write_json(output / "capture-summary.json", summary)
    print(f"INCOMPLETE CAPTURE: {summary}. Results: {output}", flush=True)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "artifacts" /
                        ("live-capture-" + datetime.now().strftime("%Y%m%d-%H%M%S")))
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.timeout > 600:
        parser.error("timeout must be between 0 and 600 seconds")
    try:
        return record(args.out_dir, args.timeout)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"CAPTURE ERROR: {exc}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
