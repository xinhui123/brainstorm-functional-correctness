"""Telemetry integrity and characterization of the original bridge score."""

import csv
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from bridge_harness import ROOT, analyze, prepare


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "artifacts")
        self.path = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def score(self, heights, extra=None):
        rows = []
        for time, height in enumerate(heights):
            rows.extend([[time, "ID_Ballast", 5 + time * 100],
                         [time, "ID_Ballast", 0, height, 0]])
        rows.extend(extra or [])
        raw = self.path / "raw.csv"
        with raw.open("w", newline="") as stream:
            csv.writer(stream).writerows(rows)
        before = raw.read_bytes()
        result = analyze(raw, self.path / "result.json")
        self.assertEqual(raw.read_bytes(), before)
        return result

    def test_supported_trace_passes(self):
        result = self.score([5, 5, 5, 5])
        self.assertTrue(result["legacy_pass"])
        self.assertEqual(result["metrics"]["hold_time_above_threshold"], 3)

    def test_early_collapse_fails(self):
        self.assertFalse(self.score([5, 3, 2])["legacy_pass"])

    def test_legacy_score_can_pass_despite_later_collapse(self):
        result = self.score([5, 5, 5, 3])
        self.assertTrue(result["legacy_pass"])
        self.assertEqual(result["metrics"]["min_height"], 3)

    def test_unrealistic_initial_height_fails(self):
        self.assertFalse(self.score([21, 21, 21])["legacy_pass"])

    def test_duplicate_clipboard_rows_do_not_inflate_time(self):
        duplicate = [[1, "ID_Ballast", 105], [1, "ID_Ballast", 0, 5, 0]]
        self.assertEqual(self.score([5, 5, 5], duplicate)["position_samples"], 3)

    def test_conflicting_samples_rejected(self):
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            self.score([5, 5, 5], [[1, "ID_Ballast", 0, 3, 0]])

    def test_missing_telemetry_is_infrastructure_error(self):
        raw = self.path / "empty.csv"
        raw.write_text("0, ID_0, 0, 5, 0\n")
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            analyze(raw, self.path / "result.json")

    def test_nan_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid numeric"):
            self.score([5, float("nan"), 5])

    def test_preparation_embeds_original_load_protocol_without_running_game(self):
        result = prepare(self.path / "prepared")
        self.assertFalse(result["simulation_executed"])
        self.assertEqual(result["captured_request"]["duration"], 17)
        machine = ET.parse(result["machine_bsg"])
        script = machine.find("./Data/StringArray[@key='lua_data']").text
        self.assertIn("local mass_max = 1500.0", script)
        self.assertIn("local ramp_duration = 15.0", script)
        self.assertIn("ID_Ballast", script)
        self.assertTrue(Path(result["custom_level"]).is_file())


if __name__ == "__main__":
    unittest.main()
