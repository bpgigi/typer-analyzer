import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from z3 import Int, And, Or
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3ComplexConstraints(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_complex_logic(self):
        # Test (x > 0 AND x < 5) OR (x > 10 AND x < 15)
        x = self.analyzer.create_int_var("x")

        condition = Or(And(x > 0, x < 5), And(x > 10, x < 15))
        self.analyzer.add_constraint(condition)

        self.assertEqual(self.analyzer.check_constraints(), "sat")
        model = self.analyzer.get_model()
        val = model[x].as_long()
        self.assertTrue((0 < val < 5) or (10 < val < 15))

    def test_reset(self):
        x = self.analyzer.create_int_var("x")
        self.analyzer.add_constraint(x > 0)
        self.analyzer.reset()

        self.assertEqual(len(self.analyzer.constraints), 0)
        self.assertEqual(len(self.analyzer.variables), 0)


if __name__ == "__main__":
    unittest.main()
