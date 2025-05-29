#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient class in client.py.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient methods."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test the org method returns correct org data."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns the correct value from org."""
        with patch.object(
            GithubOrgClient, 'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://example.com/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://example.com/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns the list of repos."""
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient, '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://example.com/orgs/test/repos"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with(mock_url.return_value)

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filtering."""
        mock_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}}
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient, '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("test")
            repos = client.public_repos(license="mit")
            self.assertEqual(repos, ["repo1", "repo3"])


class TestHasLicense(unittest.TestCase):
    """Test the has_license static method."""

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test if has_license returns correct boolean."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [
    (
        TEST_PAYLOAD[0],
        TEST_PAYLOAD[1],
        TEST_PAYLOAD[2],
        TEST_PAYLOAD[3]
    ),
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks for get_json."""
        cls.get_patcher = patch('client.get_json', side_effect=[
            cls.org_payload,
            cls.repos_payload
        ])
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down patchers."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filtering."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
