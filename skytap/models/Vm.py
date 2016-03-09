"""Support for a VM resource in Skytap."""
import json

from skytap.framework.ApiClient import ApiClient
from skytap.framework.Suspendable import Suspendable
import skytap.framework.Utils as Utils
from skytap.models.Interfaces import Interfaces
from skytap.models.Notes import Notes
from skytap.models.SkytapResource import SkytapResource
from skytap.models.UserData import UserData


class Vm(SkytapResource, Suspendable):

    """One Skytap VM."""

    def __init__(self, vm_json):
        """Init is mainly handled by the parent class."""
        super(Vm, self).__init__(vm_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Specifically, boolean values to more easily determine state, allowing
        things like 'if vm.running:' to be used.
        """
        self.data['running'] = self.runstate == 'running'
        self.data['busy'] = self.runstate == 'busy'
        self.data['suspended'] = self.runstate == 'suspended'

    def __getattr__(self, key):
        """Load values for anything that doesn't get loaded by default.

        For user_data, notes, and interfaces, a secondary API call is needed.
        Only make that call when the info is requested.
        """
        if key == 'user_data':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url + '/user_data.json')
            self.user_data = UserData(json.loads(user_json), self.url)
            return self.user_data

        if key == 'notes':
            api = ApiClient()
            notes_json = api.rest(self.url + '/notes.json')
            self.notes = Notes(notes_json, self.url)
            return self.notes

        if key == 'interfaces':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            interfaces_json = json.loads(api.rest(self.url))
            self.interfaces = Interfaces(interfaces_json["interfaces"], self.url)
            return self.interfaces

        return super(Vm, self).__getattr__(key)

    def delete(self):
        """Delete a VM.

        In general, it'd seem wise not to do this very often.
        """
        Utils.info('Deleting VM: ' + str(self.id) + '(' + self.name + ')')
        api = ApiClient()
        response = api.rest(self.url,
                            {},
                            'DELETE')
        return response
