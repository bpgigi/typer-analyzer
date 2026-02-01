import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import csv
from pathlib import Path
from analyzers.dynamic_tracer import DynamicTracer


class TestTracerFormat(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_tracer_format")
        self.test_dir.mkdir(exist_ok=True)
        self.tracer = DynamicTracer(trace_dir=str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if Path("formatted_summary.csv").exists():
            Path("formatted_summary.csv").unlink()

    def test_csv_headers(self):
        # Create dummy log to ensure stats are generated
        with open(self.test_dir / "callback_test_123.log", "w") as f:
            f.write("dummy")

        self.tracer.export_summary_csv("formatted_summary.csv")

        with open("formatted_summary.csv", "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(headers, ["Metric", "Value", "Description"])

            row = next(reader)
            self.assertEqual(row[0], "Total Traces")


if __name__ == "__main__":
    unittest.main()
