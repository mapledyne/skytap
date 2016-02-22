import yaml


class UserData(object):
    def __init__(self, contents):
        self.parse_yaml(contents)
