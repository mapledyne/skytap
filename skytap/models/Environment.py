import json
from skytap.framework.ApiClient import ApiClient
from skytap.framework.Suspendable import Suspendable
from skytap.models.Notes import Notes
from skytap.models.SkytapResource import SkytapResource
import time


class Environment(SkytapResource, Suspendable):
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

        if key == 'notes':
            api = ApiClient()
            notes_json = api.rest(self.url + '/notes.json')
            self.notes = Notes(notes_json, self.url)
            return self.notes

        return super(Environment, self).__getattr__(key)
