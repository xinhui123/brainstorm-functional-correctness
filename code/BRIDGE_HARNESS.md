# Structured bridge-test harness

The first step reuses BuildArena's original Support Lv.1 preparation and scoring from pinned commit `c3005b90686ea6dae9a69a293e7f6395eae77c9c`. Source and license are in `baseline/BuildArena`; integrity hashes are in `baseline/buildarena-source.json`.

This wrapper prepares files inside the research workspace and scores exported telemetry. It does not launch the game, send keyboard/mouse events, or copy into Steam. No LLM API keys or training are needed.

## Offline commands

Run from the research workspace:

```bash
.venv/bin/python code/bridge_harness.py doctor --output artifacts/harness-validation/doctor.json
.venv/bin/python code/bridge_harness.py prepare --out-dir artifacts/bridge-preparation-001
.venv/bin/ruff check code/bridge_harness.py code/tests
PYTHONPATH=code .venv/bin/python -m unittest discover -s code/tests -v
```

Preparation creates a handwritten short-span plumbing fixture and runs the original support preprocessing with GUI execution intercepted. It is not an LLM-generated bridge or a measured benchmark failure. Do not use synthetic tests to report repair performance. A supplied BuildArena operation-history list can be prepared with `--machine-json`; assembly histories are not supported by this wrapper yet.

## Existing test behavior

The selected level has a five-unit gap. Upstream preprocessing adds a ballast payload and embeds Lua that ramps its mass from 5 to 1500 over 15 seconds. The original automation requests 17 seconds of wall-clock execution; actual simulation times come from telemetry.

The original score passes when accumulated sampled time at/above height 4 reaches two seconds and initial height is no greater than 20. This can pass despite a subsequent collapse. It is being reused for harness compatibility, not frozen as the final research verifier. The coordinate labels differ between game and user conventions; the scorer reads vertical height from CSV column four (1-based).

The wrapper rejects missing, nonfinite, or mismatched ballast position/mass data as infrastructure errors, preserving the raw log. Repeated clipboard rows are deduplicated; distinct samples with equal timestamps are retained because the original Lua rounds time to one decimal at a higher sampling rate. For accepted logs, the original height/load calculations and Boolean criterion are unchanged. These input-integrity checks are an adapter change, not a repair-method improvement.

## Live test still required

Prepared artifacts contain `game-staging/research_support_soft.blv` and `game-staging/research_bridge_fixture_sim.bsg`. After installation into the game's CustomLevels/SavedMachines directories, open the custom level in Besiege's Level Editor, load the fixture, enable the Lua Scripting Mod, and inspect its log panel. Preserve unsaved work before this manual test.

The observed Lua Log window rolls over: a single end-of-run copy contained only 301 rows spanning the last six seconds, with one unpaired boundary entry. Copying once after 17 seconds is insufficient. Do not combine snippets from separate simulation runs or score a late tail as a complete evaluation.

Use the clipboard recorder below, which saves only ballast telemetry while it runs. It ignores the clipboard initially present, requires the beginning of a fresh run, combines overlapping copies, and scores only after paired data cover at least 17 simulation seconds without a gap larger than 0.12 seconds and show the target mass of 1500 at/after second 17. These are capture-integrity requirements, not changes to the upstream physical score. Its rolling-buffer behavior is unit-tested; live clipboard polling remains to be validated.

```bash
.venv/bin/python code/record_bridge_clipboard.py
```

When the terminal prints READY, reload the fixture and start a fresh run at 100% speed. Click the black Log panel, press Command+A then Command+C every 2–3 seconds, staying in Besiege throughout. Stop after 17 seconds and make a final copy. Return to the terminal; CAPTURE COMPLETE means a full trace was saved and scored under the new timestamped artifacts/live-capture directory. An incomplete result retains collected data for diagnosis. Each recorder invocation is for one run; do not reset/restart a simulation while recording. Default recorder timeout is three minutes and Ctrl+C ends it early. It sends no game inputs and changes no physics or scripts. Automatic GUI control remains unvalidated on this Mac.

```bash
.venv/bin/python code/bridge_harness.py analyze --csv path/to/live.csv --output artifacts/live-smoke/result.json
```

Success at this stage means a valid live trace is captured and scored, including an expected failure if the fixture cannot span the gap. It does not demonstrate repair-agent effectiveness. Audit and freeze the final verifier before running the agreed three-attempt repair comparison.
