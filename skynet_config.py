"""Handle the config file and such for the Skynet system."""
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("You do not have the 'yaml' module installed. " +
                     "Please see http://pyyaml.org/wiki/PyYAMLDocumentation " +
                     "for more information.")
    exit(1)


class SkytapConfig(object):

    """Contain all of our config values into this object.

    Read from a standard config file (config.yml by default) and then
    look for similar values in the environment to override the ones in
    config.yml. This allows us to have an empty "token" value in the config
    file, and instead use a "SKYTAP_TOKEN" environment variable.

    See comments in the config.yml file for specifics on what the variables
    do, and which ones should be in the environment variables instead.
    """

    def __init__(self,
                 config_path=os.path.dirname(os.path.realpath(sys.argv[0])) +
                 "/config.yml"):
        """Load config values and set up object.

        Default load path is config.yml in the directory the script is in.
        """
        self.config_path = config_path
        try:
            with open(self.config_path) as f:
                self.config_data = yaml.safe_load(f)
        except IOError:
            sys.stderr.write("There is no config.yml in the directory."
                             "Create one and then try again.\nFor " +
                             "reference, check config_template.yml and " +
                             "follow the listed guidelines.\n")
            exit(1)
        for key in self.config_data:
            env_val = "SKYTAP_" + key.upper()
            if env_val in os.environ:
                self.config_data[key] = os.environ[env_val]

    def __getattr__(self, key):
        """Make the config values accessible.

        This allows all config values to be available via calls like:
        config.user
        """
        if key not in self.config_data:
            raise AttributeError
        return self.config_data[key]

    def __str__(self):
        """A string represntation of the config, YAML formatted, and prettified.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = self.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config, default_flow_style=False)

    def __repr__(self):
        """A string represntation of the config, YAML formatted.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = self.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config)

    def __dir__(self):
        """List only items in the config_data list.

        Polite since we're implementing __getattr__.
        """
        dir_list = []
        for config_item in config_data:
            dir_list.append(config_item)
        return dir_list

    def __nonzero__(self):
        """Return False if there are no config items."""
        return len(config_data) > 0

    def __len__(self):
        """Expose how many config items we have."""
        return len(config_data)

    def __contains__(self, item):
        """Allow checks for items in the config list."""
        return item in config_data

    def __iter__(self):
        """Allow 'for x in config'."""
        return iter(self.config_data)

config = SkytapConfig()
