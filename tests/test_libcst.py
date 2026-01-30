import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.libcst_analyzer import LibCSTAnalyzer, CoverageStats


class TestLibCSTAnalyzer(unittest.TestCase):
    def setUp(self):
        self.test_code = """
def func_no_types(a, b):
    return a + b

def func_with_types(x: int, y: str) -> bool:
    return True

def func_partial(a: int, b) -> None:
    pass
"""
        self.test_dir = Path("test_repo")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "test.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = LibCSTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_parse_file(self):
        result = self.analyzer.parse_file(self.test_file)
        self.assertIsNotNone(result)

    def test_analyze_file(self):
        self.analyzer.analyze_file(self.test_file)
        self.assertGreater(len(self.analyzer.type_annotations), 0)

    def test_coverage_stats(self):
        self.analyzer.analyze_file(self.test_file)
        stats = self.analyzer.calculate_coverage()
        self.assertIsInstance(stats, CoverageStats)
        self.assertGreater(stats.total_functions, 0)

    def test_export_report(self):
        self.analyzer.analyze_file(self.test_file)
        output_path = Path("test_coverage.json")
        self.analyzer.export_coverage_report(output_path)
        self.assertTrue(output_path.exists())
        if output_path.exists():
            output_path.unlink()


if __name__ == "__main__":
    unittest.main()
