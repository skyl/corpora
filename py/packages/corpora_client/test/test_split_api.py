# coding: utf-8

"""
    Corpora API

    API for managing and processing corpora

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from corpora_client.api.split_api import SplitApi


class TestSplitApi(unittest.TestCase):
    """SplitApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SplitApi()

    def tearDown(self) -> None:
        pass

    def test_get_split(self) -> None:
        """Test case for get_split

        Get Split
        """
        pass

    def test_list_splits_for_file(self) -> None:
        """Test case for list_splits_for_file

        List Splits For File
        """
        pass

    def test_vector_search(self) -> None:
        """Test case for vector_search

        Vector Search
        """
        pass


if __name__ == "__main__":
    unittest.main()