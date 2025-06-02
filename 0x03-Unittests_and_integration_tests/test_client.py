#!/usr/bin/env python3
"""Test module for client.py"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized_class([
        {"org_payload": {"login": "google", "repos_url": "http://api.github.com/orgs/google/repos"},
         "repos_payload": [{"name": "repo1"}, {"name": "repo2"}],
         "expected_repos": ["repo1", "repo2"],
         "org_name": "google"}
    ])
    class TestPublicRepos(unittest.TestCase):
        """Integration-like tests with mock payloads"""
        def setUp(self):
            patcher_org = patch("client.get_json", side_effect=[self.org_payload, self.repos_payload])
            self.mock_get_json = patcher_org.start()
            self.addCleanup(patcher_org.stop)

        def test_public_repos(self):
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client.public_repos(), self.expected_repos)
            self.mock_get_json.assert_called()

    @patch("client.get_json")
    def test_org(self, mock_get_json):
        """Test org method"""
        test_payload = {"login": "google"}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient("google")
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test _public_repos_url"""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url.com"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://some_url.com")

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filtering"""
        mock_get_json.side_effect = [
            {"repos_url": "http://some_url.com"},
            [
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}},
                {"name": "repo3"},
            ]
        ]
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(license="mit"), ["repo1"])


if __name__ == '__main__':
    unittest.main()
