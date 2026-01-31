import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer


class TestComplexity(unittest.TestCase):
    def setUp(self):
        self.test_code = """
def simple_func():
    return True

def complex_func(x):
    if x > 0:
        if x > 10:
            return 1
        else:
            return 0
    for i in range(x):
        try:
            print(i)
        except:
            pass
    return -1
"""
        self.test_dir = Path("test_repo_ast")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "complexity.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = ASTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_complexity_calculation(self):
        self.analyzer.analyze_file(self.test_file)

        simple = next(f for f in self.analyzer.functions if f.name == "simple_func")
        self.assertEqual(simple.complexity, 1)

        complex_f = next(f for f in self.analyzer.functions if f.name == "complex_func")
        self.assertGreater(complex_f.complexity, 3)


if __name__ == "__main__":
    unittest.main()
