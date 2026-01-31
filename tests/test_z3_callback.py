import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3Callback(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_callback_reachability(self):
        x = self.analyzer.create_int_var("x")
        y = self.analyzer.create_int_var("y")

        self.analyzer.add_constraint(x > 10)
        self.analyzer.add_constraint(y < 5)

        self.assertEqual(self.analyzer.check_constraints(), "sat")

    def test_unreachable_path(self):
        x = self.analyzer.create_int_var("x")
        self.analyzer.add_constraint(x > 10)
        self.analyzer.add_constraint(x < 5)

        self.assertEqual(self.analyzer.check_constraints(), "unsat")


if __name__ == "__main__":
    unittest.main()
