from skytap.models.SkytapResource import SkytapResource
import json


class Environment(SkytapResource):
    def __init__(self, env_json):
        super(Environment, self).__init__(env_json)

    def _calculate_custom_data(self):
        self.running = self.runstate == 'running'
        self.busy = self.runstate == 'busy'
