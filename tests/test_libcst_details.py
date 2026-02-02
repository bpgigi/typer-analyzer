import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.libcst_analyzer import LibCSTAnalyzer


class TestLibCSTDetails(unittest.TestCase):
    def setUp(self):
        self.test_code = """
from typing import List, Optional, Dict

def complex_func(items: List[str], mapping: Dict[str, int]) -> Optional[str]:
    return items[0] if items else None
"""
        self.test_dir = Path("test_repo_details")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "complex.py"
        with open(self.test_file, "w") as f:
            f.write(self.test_code)

        self.analyzer = LibCSTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_generic_types_analysis(self):
        self.analyzer.analyze_file(self.test_file)
        stats = self.analyzer.get_annotation_stats()
        self.assertIsInstance(stats, dict)


if __name__ == "__main__":
    unittest.main()
