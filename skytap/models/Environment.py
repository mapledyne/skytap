from skytap.models.SkytapResource import SkytapResource
from skytap.framework.ApiClient import ApiClient
import json
import time


class Environment(SkytapResource):
    def __init__(self, env_json):
        super(Environment, self).__init__(env_json)

    def _calculate_custom_data(self):
        self.running = self.runstate == 'running'
        self.busy = self.runstate == 'busy'
        self.suspended = self.runstate == 'suspended'

    def __getattr__(self, key):
        if key == 'user_data':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url + '/user_data.json')
            self.user_data = json.loads(user_json)['contents']
            return self.user_data
        return super(Environment, self).__getattr__(key)

    def suspend(self, wait=False):
        self.change_state('suspended', wait)

    def run(self, wait=False):
        self.change_state('running', wait)

    def change_state(self, state, wait=False):
        self.refresh()
        if self.runstate == state:
            return True
        api = ApiClient()
        url = self.url + '.json'
        data = {"runstate": state}
        response = api.rest(url, {}, 'PUT', data)
        if not wait:
            return True

        self.refresh()
        counter = 0
        while not self.runstate == state and counter < 10:
            time.sleep(10)
            self.refresh()
        if self.runstate == state:
            return True
        return False
