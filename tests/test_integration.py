import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer
from analyzers.libcst_analyzer import LibCSTAnalyzer
from collectors.commit_collector import CommitCollector


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_integration_repo")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "app.py"
        with open(self.test_file, "w") as f:
            f.write("def main(): pass")

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_pipeline(self):
        ast_analyzer = ASTAnalyzer(str(self.test_dir))
        ast_analyzer.analyze_file(self.test_file)
        self.assertEqual(len(ast_analyzer.functions), 1)

        cst_analyzer = LibCSTAnalyzer(str(self.test_dir))
        cst_analyzer.analyze_file(self.test_file)

        collector = CommitCollector(str(self.test_dir))
        self.assertIsNotNone(collector)


if __name__ == "__main__":
    unittest.main()
