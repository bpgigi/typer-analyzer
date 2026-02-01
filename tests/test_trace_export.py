import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.dynamic_tracer import DynamicTracer


class TestTraceExport(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_trace_export")
        self.test_dir.mkdir(exist_ok=True)
        self.tracer = DynamicTracer(trace_dir=str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if Path("summary.csv").exists():
            Path("summary.csv").unlink()

    def test_csv_export(self):
        # Create a dummy log file to simulate data
        with open(self.test_dir / "callback_test_123.log", "w") as f:
            f.write("dummy trace data")

        self.tracer.export_summary_csv("summary.csv")
        self.assertTrue(Path("summary.csv").exists())

        with open("summary.csv", "r") as f:
            content = f.read()
            self.assertIn("total_callbacks", content)


if __name__ == "__main__":
    unittest.main()
