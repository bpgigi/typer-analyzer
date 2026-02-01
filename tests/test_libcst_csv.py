import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import csv
from pathlib import Path
from analyzers.libcst_analyzer import LibCSTAnalyzer


class TestLibCSTCSV(unittest.TestCase):
    def setUp(self):
        self.test_code = """
def test_func(x: int):
    pass
"""
        self.test_dir = Path("test_repo_csv")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "test.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = LibCSTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if Path("types.csv").exists():
            Path("types.csv").unlink()

    def test_csv_export(self):
        self.analyzer.analyze_file(self.test_file)
        self.analyzer.export_to_csv("types.csv")

        self.assertTrue(Path("types.csv").exists())

        with open("types.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["function"], "test_func")
            self.assertEqual(rows[0]["annotation"], "int")


if __name__ == "__main__":
    unittest.main()
