import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from collectors.github_collector import GitHubCollector


class TestGithubPagination(unittest.TestCase):
    @patch("requests.get")
    def test_pagination(self, mock_get):
        # Mock responses for 2 pages
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = [{"id": 1}, {"id": 2}]
        mock_resp1.links = {"next": {"url": "..."}}
        mock_resp1.status_code = 200

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = [{"id": 3}]
        mock_resp2.links = {}  # No next page
        mock_resp2.status_code = 200

        mock_get.side_effect = [mock_resp1, mock_resp2]

        collector = GitHubCollector("owner/repo", "token")
        # Access private method for testing
        results = collector._collect_paginated("http://api.github.com/test")

        self.assertEqual(len(results), 3)
        self.assertEqual(mock_get.call_count, 2)


if __name__ == "__main__":
    unittest.main()
