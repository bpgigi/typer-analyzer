import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3CLI(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_cli_param_validation(self):
        violations = self.analyzer.verify_parameter_constraints(
            "count", 5, ["count > 0", "count < 10"]
        )
        self.assertEqual(len(violations), 0)

        violations = self.analyzer.verify_parameter_constraints(
            "count", -1, ["count > 0"]
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].variable, "count")
        self.assertIn("violates", violations[0].message)

    def test_string_param(self):
        violations = self.analyzer.verify_parameter_constraints(
            "mode", "prod", ["mode == 'dev'"]
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].variable, "mode")


if __name__ == "__main__":
    unittest.main()
