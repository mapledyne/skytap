"""Support for an Environment resource in Skytap."""
import json
import logging
from skytap.framework.ApiClient import ApiClient
from skytap.framework.Suspendable import Suspendable
from skytap.models.Notes import Notes
from skytap.models.SkytapResource import SkytapResource
from skytap.models.UserData import UserData
from skytap.models.Vms import Vms


class Environment(SkytapResource, Suspendable):

    """One Skytap environment."""

    def __init__(self, env_json):
        """Init is mainly handled by the parent class."""
        super(Environment, self).__init__(env_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Specifically, boolean values to more easily determine state, allowing
        things like 'if env.running:' to be used.
        """
        self.data['running'] = self.runstate == 'running'
        self.data['busy'] = self.runstate == 'busy'
        self.data['suspended'] = self.runstate == 'suspended'
        self.data['vms'] = Vms(self.vms, self.id)

    def __getattr__(self, key):
        """Load values for anything that doesn't get loaded by default.

        For user_data and notes, a secondary API call is needed. Only make that
        call when the info is requested.
        """
        if key == 'user_data':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url + '/user_data.json')
            self.data['user_data'] = UserData(json.loads(user_json), self.url)
            return self.user_data

        if key == 'notes':
            api = ApiClient()
            notes_json = api.rest(self.url + '/notes.json')
            self.notes = Notes(notes_json, self.url)
            return self.notes

        return super(Environment, self).__getattr__(key)

    def delete(self):
        """Delete the environment.

        In general, it'd seem wise not to do this very often.
        """
        logging.info('Deleting environment: ' +
                     str(self.id) + '(' + self.name + ')')
        api = ApiClient()
        response = api.rest(self.url_v1,
                            {},
                            'DELETE')
        return response
