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
    def __init__(self,
                 config_path=os.path.dirname(os.path.realpath(sys.argv[0])) +
                 "/config.yml"):
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
        if key not in self.config_data:
            raise AttributeError
        return self.config_data[key]

    def __str__(self):
        temp_config = self.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config, default_flow_style=False)

    def __repr__(self):
        temp_config = self.config_data.copy()
        temp_config["token"] = ''
        return yaml.dump(temp_config)

    def __dir__(self):
        dir_list = []
        for config_item in config_data:
            dir_list.append(config_item)
        return dir_list

    def __nonzero__(self):
        return len(config_data) > 0

    def __len__(self):
        return len(config_data)

    def __contains__(self, item):
        return item in config_data

    def __iter__(self):
        return iter(self.config_data)

config = SkytapConfig()
