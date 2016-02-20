"""Handle the config file and such for the Skynet system."""
import os
import sys
import yaml
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class _NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ConfigType(type):
    def __getattr__(cls, key):
        """Make the config values accessible.

        This allows all config values to be available via calls like:
        Config.user
        """
        if key not in cls.config_data:
            raise AttributeError
        return cls.config_data[key]

    def __len__(cls):
        """Expose how many config items we have."""
        return len(cls.config_data)

    def __str__(cls):
        """A string represntation of the config, YAML formatted, and prettified.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config, default_flow_style=False)

    def __repr__(cls):
        """A string represntation of the config, YAML formatted.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config)

    def __dir__(cls):
        """List only items in the config_data list.

        Polite since we're implementing __getattr__.
        """
        dir_list = []
        for config_item in cls.config_data:
            dir_list.append(config_item)
        return dir_list

    def __nonzero__(cls):
        """Return False if there are no config items."""
        return len(cls.config_data) > 0


    def __contains__(cls, item):
        """Allow checks for items in the config list."""
        return item in cls.config_data

    def __iter__(cls):
        """Allow 'for x in config'."""
        return iter(cls.config_data)


class Config(object):

    """Contain all of our config values into this object.

    Read from a standard config file (config.yml by default) and then
    look for similar values in the environment to override the ones in
    config.yml. This allows us to have an empty "token" value in the config
    file, and instead use a "SKYTAP_TOKEN" environment variable.

    See comments in the config.yml file for specifics on what the variables
    do, and which ones should be in the environment variables instead.
    """
    __metaclass__ = ConfigType
    # Some very basic defaults. This will allow the module to work by
    # just creating the SKYTAP_TOKEN and SKYTAP_USER env variables
    # for most things you'd want to do.
    config_data = {'user': '',
                        'token': '',
                        'log_level': 30,
                        'base_url': 'https://cloud.skytap.com'
                        }


# Load config values and set up the class.

for key in Config.config_data:
    env_val = "SKYTAP_" + key.upper()
    if env_val in os.environ:
        Config.config_data[key] = os.environ[env_val]

# Change the log level of the requests object, if appropriate.
logger.setLevel(int(Config.log_level))
logging.getLogger("requests").setLevel(logging.WARNING)
if (int(Config.log_level) < logging.INFO):
    logging.getLogger("requests").setLevel(int(Config.log_level))
