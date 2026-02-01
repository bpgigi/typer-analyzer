import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from analyzers.dynamic_tracer import DynamicTracer


class TestVariableTrace(unittest.TestCase):
    def setUp(self):
        self.tracer = DynamicTracer(trace_dir="test_var_traces")

    def tearDown(self):
        import shutil

        if os.path.exists("test_var_traces"):
            shutil.rmtree("test_var_traces")

    def test_trace_specific_vars(self):
        def sample_func(a, b):
            x = a + b
            y = x * 2
            return y

        self.tracer.trace_function_vars(sample_func, watch_vars=["x", "y"])

        expected_log = self.tracer.trace_dir / "vars_sample_func.log"
        pass


if __name__ == "__main__":
    unittest.main()
