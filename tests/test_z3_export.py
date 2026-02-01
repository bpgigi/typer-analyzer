import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import csv
from pathlib import Path
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3Export(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()
        self.test_file = Path("z3_results.csv")

    def tearDown(self):
        if self.test_file.exists():
            self.test_file.unlink()

    def test_csv_export(self):
        results = [
            {
                "type": "cli_param",
                "variable": "count",
                "constraint": "count > 0",
                "status": "violated",
                "value": -1,
            },
            {
                "type": "callback_path",
                "variable": "on_click",
                "constraint": "reachable",
                "status": "sat",
                "value": "true",
            },
        ]

        self.analyzer.export_analysis_csv(str(self.test_file), results)

        self.assertTrue(self.test_file.exists())

        with open(self.test_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["variable"], "count")
            self.assertEqual(rows[1]["status"], "sat")


if __name__ == "__main__":
    unittest.main()
