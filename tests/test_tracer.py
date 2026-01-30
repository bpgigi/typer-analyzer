import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.dynamic_tracer import DynamicTracer, CallbackTrace


class TestDynamicTracer(unittest.TestCase):
    def setUp(self):
        self.tracer = DynamicTracer(trace_dir="test_traces")

    def tearDown(self):
        import shutil

        if Path("test_traces").exists():
            shutil.rmtree("test_traces")

    def test_init(self):
        self.assertTrue(self.tracer.trace_dir.exists())

    def test_trace_callback(self):
        def test_callback():
            return "test"

        trace = self.tracer.trace_callback(test_callback, "test_trigger")
        self.assertIsInstance(trace, CallbackTrace)
        self.assertEqual(trace.callback_name, "test_callback")
        self.assertEqual(trace.trigger_event, "test_trigger")

    def test_export_callback_report(self):
        output_path = Path("test_callback_report.json")
        self.tracer.export_callback_report(output_path)
        self.assertTrue(output_path.exists())
        if output_path.exists():
            output_path.unlink()

    def test_get_trace_summary(self):
        summary = self.tracer.get_trace_summary()
        self.assertIn("total_traces", summary)
        self.assertIn("trace_directory", summary)


if __name__ == "__main__":
    unittest.main()
