import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.framework.Config import Config  # nopep8


class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic_config_check(self):
        self.assertTrue(len(Config) > 0, 'No config values found.')
        self.assertTrue(len(Config.user) > 0, 'Skytap user missing. ' +
                        'Define SKYTAP_USER env variable.')
        self.assertTrue(len(Config.token) > 0, 'Skytap token missing. ' +
                        'Define SKYTAP_TOKEN env variable.')
        self.assertTrue(len(Config.base_url) > 0, 'Skytap base_url ' +
                        'missing. Define SKYTAP_BASE_URL env variable.')
        self.assertTrue(Config.base_url == 'https://cloud.skytap.com',
                        'Base_url should always be http://cloud.skytap.com.')
        with self.assertRaises(AttributeError):
            place_holder = Config.this_value_should_not_exist
