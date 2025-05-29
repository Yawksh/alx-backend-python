from parameterized import parameterized_class
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect for mock get."""
            if url == "https://api.github.com/orgs/google":
                return Mock(json=lambda: cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return Mock(json=lambda: cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test public_repos."""
        test_class = GithubOrgClient('google')
        self.assertEqual(test_class.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public_repos with license."""
        test_class = GithubOrgClient('google')
        self.assertEqual(test_class.public_repos(license="apache-2.0"),
                         self.apache2_repos)