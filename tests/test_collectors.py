import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from collectors.commit_collector import CommitCollector
from collectors.github_collector import GitHubCollector


class TestCollectors(unittest.TestCase):
    @patch("collectors.commit_collector.Repository")
    def test_commit_collector(self, mock_repo):
        mock_commit = MagicMock()
        mock_commit.hash = "abc1234"
        mock_commit.msg = "test commit"
        mock_commit.author.name = "Tester"
        mock_commit.author.email = "test@example.com"
        mock_commit.author_date = MagicMock()
        mock_commit.author_date.__lt__ = MagicMock(return_value=False)
        mock_commit.author_date.__gt__ = MagicMock(return_value=False)
        mock_commit.modified_files = []
        mock_commit.insertions = 10
        mock_commit.deletions = 5

        mock_repo.return_value.traverse_commits.return_value = [mock_commit]

        collector = CommitCollector("dummy_path")
        commits = collector.collect()

        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0].hash, "abc1234")
        self.assertEqual(commits[0].author, "Tester")

    def test_github_collector_init(self):
        collector = GitHubCollector(token="test_token")
        self.assertIsNotNone(collector.session)
        self.assertIn("Authorization", collector.headers)


if __name__ == "__main__":
    unittest.main()
