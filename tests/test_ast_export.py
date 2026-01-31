import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import csv
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer


class TestASTExport(unittest.TestCase):
    def setUp(self):
        self.test_code = '''
def sample_func(a, b):
    """A sample function"""
    return a + b

class SampleClass:
    pass
'''
        self.test_dir = Path("test_repo_export")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "sample.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = ASTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if Path("test_output.csv").exists():
            Path("test_output.csv").unlink()

    def test_csv_export(self):
        self.analyzer.analyze_file(self.test_file)
        output_file = "test_output.csv"
        self.analyzer.export_to_csv(output_file)

        self.assertTrue(Path(output_file).exists())

        with open(output_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 2)

            func_row = next(r for r in rows if r["name"] == "sample_func")
            self.assertEqual(func_row["type"], "function")
            self.assertEqual(int(func_row["docstring_len"]), len("A sample function"))


if __name__ == "__main__":
    unittest.main()
