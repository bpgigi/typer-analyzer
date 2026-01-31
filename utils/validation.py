from typing import Dict, List, Any
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

    def validate_commits_data(self, commits_file: str = "commits.json") -> bool:
        path = self.data_dir / commits_file
        if not path.exists():
            logger.error(f"Commits file not found: {path}")
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                commits = json.load(f)

            if not isinstance(commits, list):
                logger.error("Commits data must be a list")
                return False

            for i, commit in enumerate(commits):
                if not all(k in commit for k in ["hash", "author", "date"]):
                    logger.error(f"Commit at index {i} missing required fields")
                    return False

            return True
        except Exception as e:
            logger.error(f"Error validating commits: {e}")
            return False

    def validate_issues_data(self, issues_file: str = "issues.json") -> bool:
        path = self.data_dir / issues_file
        if not path.exists():
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                issues = json.load(f)

            if not isinstance(issues, list):
                return False

            return True
        except Exception:
            return False

    def check_data_integrity(self) -> Dict[str, bool]:
        return {
            "commits": self.validate_commits_data(),
            "issues": self.validate_issues_data(),
        }
