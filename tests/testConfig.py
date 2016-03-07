import json
import nose
import sys

sys.path.append('..')
from skytap.framework.Config import Config  # noqa
import skytap.framework.Utils as Utils  # noqa


def test_we_have_some_config_values():
    """Check to see we have some config values."""
    assert len(Config) > 0


def test_config_user_is_set():
    """Make sure the config user (SKTYAP_USER env variable) is set."""
    assert len(Config.user) > 0


def test_config_token_is_set():
    """Make sure the config token (SKYTAP_TOKEN env variable) is set."""
    assert len(Config.token) > 0


def test_config_base_url_is_set():
    """Make sure the base_url is set."""
    assert len(Config.base_url) > 0


def test_base_url_is_correct():
    """Make sure the base_url is set to http://cloud.skytap.com."""
    assert Config.base_url == 'https://cloud.skytap.com'


@nose.tools.raises(AttributeError)
def test_config_value_doesnt_exist():
    """Test that an invalid config request raises an AttributeError."""
    log_lvl = Utils.log_level()
    Utils.log_level(50)
    place_holder = Config.this_value_should_not_exist
    Utils.log_level(log_lvl)


def test_config_dir():
    """Ensure __dir__ returns reasoable results."""
    assert len(dir(Config)) == len(Config)


def test_config_repr():
    """Ensure repr() returns, but strips token."""
    check = json.loads(repr(Config))
    assert check['user'] == Config.user
    assert check['token'] == ''


def test_config_str():
    """Ensure str() returns, but strips token."""
    check = json.loads(str(Config))
    assert check['user'] == Config.user
    assert check['token'] == ''


def test_config_contains():
    assert 'user' in Config
    assert 'not_a_config' not in Config
