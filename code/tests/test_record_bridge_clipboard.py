"""Rolling-window capture must preserve early data without mixing runs."""

import unittest

from record_bridge_clipboard import Capture, ballast_rows


def samples(start, end):
    rows = []
    for tick in range(start, end + 1):
        t = tick / 25
        rows.extend([(t, "ID_Ballast", 0, 2, 0),
                     (t, "ID_Ballast", 1500 if t >= 15 else 5 + t * 80)])
    return rows


class CaptureTests(unittest.TestCase):
    def test_unrelated_clipboard_content_is_not_retained(self):
        self.assertEqual(ballast_rows("unrelated private text\n"), [])

    def test_late_tail_cannot_initialize_capture(self):
        capture = Capture()
        self.assertFalse(capture.add(samples(340, 490)))
        self.assertFalse(capture.records)

    def test_overlapping_windows_recover_all_samples(self):
        capture = Capture()
        for first, last in [(1, 100), (51, 200), (151, 300), (251, 400), (301, 450)]:
            capture.add(samples(first, last))
        self.assertTrue(capture.summary()["complete_load_window"])
        self.assertEqual(capture.summary()["position_samples"], 450)

    def test_missing_interior_window_blocks_scoring(self):
        capture = Capture()
        capture.add(samples(1, 100))
        capture.add(samples(250, 450))
        self.assertFalse(capture.summary()["complete_load_window"])

    def test_boundary_orphan_recovered_from_prior_copy(self):
        capture = Capture()
        capture.add(samples(1, 400))
        tail = samples(301, 450)
        tail.pop(1)
        capture.add(tail)
        self.assertTrue(capture.summary()["complete_load_window"])

    def test_restarted_clock_rejected(self):
        capture = Capture()
        capture.add(samples(1, 100))
        with self.assertRaisesRegex(ValueError, "restarted"):
            capture.add(samples(1, 25))


if __name__ == "__main__":
    unittest.main()
