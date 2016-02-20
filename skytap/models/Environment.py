from skytap.models.SkytapResource import SkytapResource
import json


class Environment(SkytapResource):
    def __init__(self, env_json):
        super(Environment, self).__init__(env_json)
