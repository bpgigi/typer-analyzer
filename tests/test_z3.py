import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from z3 import sat, unsat
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3Analyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_int_constraints(self):
        x = self.analyzer.create_int_var("x")
        self.analyzer.add_constraint(x > 0, "x must be positive")
        self.analyzer.add_constraint(x < 10, "x must be less than 10")

        result = self.analyzer.check_constraints()
        self.assertEqual(result, str(sat))

        model = self.analyzer.get_model()
        self.assertIsNotNone(model)
        self.assertGreater(model[x].as_long(), 0)
        self.assertLess(model[x].as_long(), 10)

    def test_unsat_constraints(self):
        y = self.analyzer.create_int_var("y")
        self.analyzer.add_constraint(y > 10)
        self.analyzer.add_constraint(y < 5)

        result = self.analyzer.check_constraints()
        self.assertEqual(result, str(unsat))
        self.assertIsNone(self.analyzer.get_model())

    def test_string_constraints(self):
        s = self.analyzer.create_string_var("s")
        from z3 import StringVal, Length

        self.analyzer.add_constraint(s == StringVal("hello"))
        self.analyzer.add_constraint(Length(s) == 5)

        result = self.analyzer.check_constraints()
        self.assertEqual(result, str(sat))


if __name__ == "__main__":
    unittest.main()
