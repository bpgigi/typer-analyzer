import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer


class TestASTPerformance(unittest.TestCase):
    def setUp(self):
        self.test_code = """
import os
import sys
from datetime import datetime

def func1():
    pass

class Class1:
    def method1(self):
        pass
"""
        self.test_dir = Path("test_repo_perf")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "perf.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = ASTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_single_pass_analysis(self):
        imports = self.analyzer.analyze_dependencies(self.test_file)
        self.assertIn("os", imports)
        self.assertIn("sys", imports)
        self.assertIn("datetime", imports)

        self.analyzer.analyze_file(self.test_file)
        self.assertEqual(len(self.analyzer.functions), 1)
        self.assertEqual(len(self.analyzer.classes), 1)


if __name__ == "__main__":
    unittest.main()
