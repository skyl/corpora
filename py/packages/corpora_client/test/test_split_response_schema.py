# coding: utf-8

"""
    Corpora API

    API for managing and processing corpora

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from corpora_client.models.split_response_schema import SplitResponseSchema

class TestSplitResponseSchema(unittest.TestCase):
    """SplitResponseSchema unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SplitResponseSchema:
        """Test SplitResponseSchema
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SplitResponseSchema`
        """
        model = SplitResponseSchema()
        if include_optional:
            return SplitResponseSchema(
                id = '',
                content = '',
                order = 56,
                file_id = ''
            )
        else:
            return SplitResponseSchema(
                id = '',
                content = '',
                order = 56,
                file_id = '',
        )
        """

    def testSplitResponseSchema(self):
        """Test SplitResponseSchema"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
