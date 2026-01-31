import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import json
from pathlib import Path
from utils.validation import DataValidator


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_data_validation")
        self.test_dir.mkdir(exist_ok=True)
        self.validator = DataValidator(str(self.test_dir))

    def tearDown(self):
        import shutil

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_valid_commits(self):
        valid_data = [
            {"hash": "abc", "author": "me", "date": "2026-01-01"},
            {"hash": "def", "author": "you", "date": "2026-01-02"},
        ]
        with open(self.test_dir / "commits.json", "w") as f:
            json.dump(valid_data, f)

        self.assertTrue(self.validator.validate_commits_data())

    def test_invalid_commits(self):
        invalid_data = [
            {"hash": "abc"},
        ]
        with open(self.test_dir / "commits.json", "w") as f:
            json.dump(invalid_data, f)

        self.assertFalse(self.validator.validate_commits_data())


if __name__ == "__main__":
    unittest.main()
