import json
import logging
import nose
import sys

sys.path.append('..')
from skytap.framework.Config import Config  # nopep8


class TestConfig(object):

    def setUp(self):
        self.previous_level = logging.root.manager.disable
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(self.previous_level)

    def test_we_have_some_config_values(self):
        """Check to see we have some config values."""
        assert len(Config) > 0

    def test_config_user_is_set(self):
        """Make sure the config user (SKTYAP_USER env variable) is set."""
        assert len(Config.user) > 0

    def test_config_token_is_set(self):
        """Make sure the config token (SKYTAP_TOKEN env variable) is set."""
        assert len(Config.token) > 0

    def test_config_base_url_is_set(self):
        """Make sure the base_url is set."""
        assert len(Config.base_url) > 0

    def test_base_url_is_correct(self):
        """Make sure the base_url is set to http://cloud.skytap.com."""
        assert Config.base_url == 'https://cloud.skytap.com'

    @nose.tools.raises(AttributeError)
    def test_config_value_doesnt_exist(self):
        """Test that an invalid config request raises an AttributeError."""
        place_holder = Config.this_value_should_not_exist
