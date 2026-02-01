import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer


class TestCallGraph(unittest.TestCase):
    def setUp(self):
        self.test_code = """
def func_a():
    func_b()

def func_b():
    print("hello")
"""
        self.test_dir = Path("test_repo_call")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "calls.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = ASTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_call_extraction(self):
        calls = self.analyzer.analyze_calls(self.test_file)

        self.assertGreater(len(calls), 0)

        found = False
        for call in calls:
            if call["source"] == "func_a" and call["target"] == "func_b":
                found = True
                break
        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()
