#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from unittest.mock import PropertyMock

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        expected_payload = {"name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

class TestGithubOrgClient(unittest.TestCase):
    # ... existing test_org method ...

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from mocked org"""
        test_url = "https://api.github.com/orgs/testorg/repos"
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": test_url}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, test_url)


if __name__ == "__main__":
    unittest.main()

