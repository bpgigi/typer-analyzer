import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock
from analyzers.z3_analyzer import Z3Analyzer
from z3 import Z3Exception


class TestZ3Error(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_solver_error_handling(self):
        self.analyzer.solver.check = MagicMock(
            side_effect=Z3Exception("Solver crashed")
        )

        result = self.analyzer.check_constraints()
        self.assertEqual(result, "error")

        model = self.analyzer.get_model()
        self.assertIsNone(model)


if __name__ == "__main__":
    unittest.main()
