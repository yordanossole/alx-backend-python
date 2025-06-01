#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class and its utilities
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        expected_payload = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected repos URL"""
        test_url = "https://api.github.com/orgs/testorg/repos"
        with patch(
            "client.GithubOrgClient.org", 
            new_callable=PropertyMock
            ) as mock_org:
            mock_org.return_value = {"repos_url": test_url}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, test_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct repo names"""
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = fake_repos_payload

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://fakeurl.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://fakeurl.com/orgs/testorg/repos"
            )


if __name__ == "__main__":
    unittest.main()
