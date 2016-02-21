import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.framework.ApiClient import ApiClient  # nopep8


class TestApiClient(unittest.TestCase):

    def setUp(self):
        self.api_client = ApiClient()

    def test_basic_api_check(self):
        response = self.api_client.rest('/configurations')
        json_check = json.loads(response)
        self.assertTrue(len(json_check) > 0, "No JSON returned.")
