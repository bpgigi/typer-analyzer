import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
import requests
from collectors.github_collector import GitHubCollector


class TestCollectorTimeout(unittest.TestCase):
    @patch("requests.Session.get")
    def test_timeout_handling(self, mock_get):
        mock_get.side_effect = requests.Timeout("Connection timed out")

        collector = GitHubCollector("token")
        # Should catch exception and return empty list (or partial results)
        results = collector.get_issues("owner", "repo")

        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
