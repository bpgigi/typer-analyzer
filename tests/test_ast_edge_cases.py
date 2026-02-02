import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from pathlib import Path
from analyzers.ast_analyzer import ASTAnalyzer


class TestASTEdgeCases(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_ast_edge")
        self.test_dir.mkdir(exist_ok=True)
        self.analyzer = ASTAnalyzer(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_empty_file(self):
        empty_file = self.test_dir / "empty.py"
        with open(empty_file, "w") as f:
            f.write("")

        self.analyzer.analyze_file(empty_file)
        self.assertEqual(len(self.analyzer.functions), 0)
        self.assertEqual(len(self.analyzer.classes), 0)

    def test_nested_functions(self):
        nested_code = """
def outer():
    def inner():
        pass
    pass
"""
        nested_file = self.test_dir / "nested.py"
        with open(nested_file, "w") as f:
            f.write(nested_code)

        self.analyzer.analyze_file(nested_file)
        # Should detect both functions
        func_names = [f.name for f in self.analyzer.functions]
        self.assertIn("outer", func_names)
        self.assertIn("inner", func_names)

    def test_async_generator(self):
        async_gen = """
async def async_gen_func():
    yield 1
"""
        gen_file = self.test_dir / "async_gen.py"
        with open(gen_file, "w") as f:
            f.write(async_gen)

        self.analyzer.analyze_file(gen_file)
        func = next(f for f in self.analyzer.functions if f.name == "async_gen_func")
        self.assertTrue(func.is_async)


if __name__ == "__main__":
    unittest.main()
