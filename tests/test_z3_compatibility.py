import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from analyzers.z3_analyzer import Z3Analyzer


class TestZ3Compatibility(unittest.TestCase):
    def setUp(self):
        self.analyzer = Z3Analyzer()

    def test_basic_compatibility(self):
        self.assertTrue(self.analyzer.check_type_compatibility("int", "int"))

        self.assertFalse(self.analyzer.check_type_compatibility("int", "str"))

    def test_union_compatibility(self):
        self.assertTrue(
            self.analyzer.check_type_compatibility("int", "Union[int, str]")
        )

        self.assertTrue(
            self.analyzer.check_type_compatibility("str", "Union[int, str]")
        )

        pass


if __name__ == "__main__":
    unittest.main()
