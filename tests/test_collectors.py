import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from collectors.commit_collector import CommitCollector
from collectors.issues_collector import IssuesCollector


class TestCollectors(unittest.TestCase):
    @patch("collectors.commit_collector.Repository")
    def test_commit_collector(self, mock_repo):
        # Mock repository behavior
        mock_commit = MagicMock()
        mock_commit.hash = "abc1234"
        mock_commit.msg = "test commit"
        mock_commit.author.name = "Tester"
        mock_commit.committer_date.isoformat.return_value = "2026-01-01"
        mock_commit.lines = 10
        mock_commit.files = 2

        mock_repo.return_value.traverse_commits.return_value = [mock_commit]

        collector = CommitCollector("dummy_path")
        commits = collector.collect_commits()

        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]["hash"], "abc1234")

    def test_issues_collector_init(self):
        collector = IssuesCollector("owner/repo", "token")
        self.assertEqual(collector.repo, "owner/repo")
        self.assertIsNotNone(collector.headers)


if __name__ == "__main__":
    unittest.main()
