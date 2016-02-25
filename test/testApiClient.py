"""Test Skytap general API client."""
import json
import sys

sys.path.append('..')
from skytap.framework.ApiClient import ApiClient  # nopep8


class TestApiClient():

    def setUp(self):
        self.api_client = ApiClient()

    def test_basic_api_check(self):
        """Some basic testing of the API client."""
        response = self.api_client.rest('/v2/configurations')
        json_check = json.loads(response)
        assert len(json_check) > 0, "JSON didn't result in any rows"
