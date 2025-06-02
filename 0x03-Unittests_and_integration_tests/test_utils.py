#!/usr/bin/env python3
"""Test module for utils.py"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        """Test access_nested_map raises KeyError on bad path"""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json"""

    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """Test get_json returns proper JSON payload"""
        test_url = "http://example.com"
        test_payload = {"payload": True}
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Unit tests for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches method results"""

        class TestClass:
            def __init__(self):
                self.call_count = 0

            @memoize
            def a_method(self):
                self.call_count += 1
                return 42

        obj = TestClass()
        self.assertEqual(obj.a_method, 42)
        self.assertEqual(obj.a_method, 42)
        self.assertEqual(obj.call_count, 1)


if __name__ == '__main__':
    unittest.main()
