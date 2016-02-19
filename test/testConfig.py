import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.framework.Config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = Config()

    def test_basic_api_check(self):
        self.assertTrue(len(self.config.user) > 0, 'Skytap user missing. ' +
                        'Define SKYTAP_USER env variable.')
        self.assertTrue(len(self.config.token) > 0, 'Skytap token missing. ' +
                        'Define SKYTAP_TOKEN env variable.')
        self.assertTrue(len(self.config.base_url) > 0, 'Skytap base_url ' +
                        'missing. Define SKYTAP_BASE_URL env variable.')

        with self.assertRaises(AttributeError):
            place_holder = self.this_value_should_not_exist
