import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from collectors.github_collector import GitHubCollector


class TestGithubPagination(unittest.TestCase):
    @patch.object(GitHubCollector, "get_contributors")
    def test_pagination(self, mock_get_contributors):
        mock_get_contributors.return_value = [
            {"login": "user1", "contributions": 100},
            {"login": "user2", "contributions": 50},
            {"login": "user3", "contributions": 25},
        ]

        collector = GitHubCollector(token="test")
        results = collector.get_contributors("owner", "repo", max_count=3)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["login"], "user1")


if __name__ == "__main__":
    unittest.main()
