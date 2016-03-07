"""Handle the config file and such for the Skytap system."""
import json
import os
import six

import skytap.framework.Utils as Utils

initial_config = {'user': '',           # Should only be defined in env vars.
                  'token': '',          # Should only be defined in env vars.
                  'log_level': 30,      # 0 - 50. Debug=10, Info=20, Warn=30
                  'base_url': 'https://cloud.skytap.com',
                  'max_http_attempts': 4,
                  'retry_wait': 10,     # Skytap recommends waiting 10 sec.
                  'add_note_on_state_change': True
                  }


class ConfigType(type):

    """A meta class for Config.

    This allows magic methods to be used on the Config class, making things
    like 'Config.token' work as well as len(Config) even when Config is a class
    and not an object. This makes for cleaner use in other classes.
    """

    def __getattr__(cls, key):
        """Make the config values accessible.

        This allows all config values to be available via calls like:
        Config.user
        """
        if key not in cls.config_data:
            # These are called during nose setup before logging is turned off
            # during testing. Not the best, but tests look better with these
            # supressed.
            if key not in ['__test__', 'address', 'im_class', '__self__']:
                Utils.error("Tried to access config value '" +
                            str(key) + "', which doesn't exist.")
            raise AttributeError
        return cls.config_data[key]

    def __len__(cls):
        """Expose how many config items we have."""
        return len(cls.config_data)

    def __str__(cls):
        """A string representation of the config, JSON formatted, and prettified.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config["token"] = ''
        return json.dumps(temp_config, indent=4)

    def __repr__(cls):
        """A string representation of the config, JSON formatted.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config["token"] = ''
        return json.dumps(temp_config)

    def __dir__(cls):
        """List only items in the config_data list.

        Polite since we're implementing __getattr__.
        """
        dir_list = []
        for config_item in cls.config_data:
            dir_list.append(config_item)
        return dir_list

    def __contains__(cls, item):
        """Allow checks for items in the config list."""
        return item in cls.config_data

    def __iter__(cls):
        """Allow 'for x in config'.

        Ultimately, this passes the 'how to iterate' problem down to the
        config_data object and lets that object handle the actual iteration.
        """
        return iter(cls.config_data)


@six.add_metaclass(ConfigType)
class Config(object):

    """Contain all of our config values into this object."""

    # Some very basic defaults. This will allow the module to work by
    # just creating the SKYTAP_TOKEN and SKYTAP_USER env variables
    # for most things you'd want to do.
    config_data = initial_config

# Load config values and set up the class.

for key in Config:
    env_val = "SKYTAP_" + key.upper()
    if env_val in os.environ:
        Config.config_data[key] = os.environ[env_val]
        try:
            Config.config_data[key] = int(Config.config_data[key])
        except ValueError:
            pass

if os.environ.get('READTHEDOCS', None) != 'True':
    if Config.base_url != 'https://cloud.skytap.com':
        Utils.warning('Base URL is not Skytap\'s recommended value. ' +
                      'This very likely will break things.')

    if len(Config.token) == 0:
        Utils.error('No environment variable SKYTAP_TOKEN found. ' +
                    'Set this variable and try again.')
        raise ValueError

    if len(Config.user) == 0:
        Utils.error('No environment variable SKYTAP_USER found. ' +
                    'Set this variable and try again.')
        raise ValueError

Utils.log_level(Config.log_level)
