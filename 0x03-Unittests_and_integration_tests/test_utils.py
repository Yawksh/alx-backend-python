from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self) -> None:
        """Test memoize decorator."""

        class TestClass:
            """Test class for memoize."""

            def a_method(self):
                """Test method."""
                return 42

            @memoize
            def a_property(self):
                """Test property."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mock_method.assert_called_once()