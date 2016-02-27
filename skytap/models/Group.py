"""Support for Skytap groups."""
import json
from skytap.framework.ApiClient import ApiClient
from skytap.models.SkytapResource import SkytapResource
from skytap.Users import Users


class Group(SkytapResource):

    def __getattr__(self, key):
        """Load values for anything that doesn't get loaded by default.

        For user_data and notes, a secondary API call is needed. Only make that
        call when the info is requested.
        """
        if key == 'users':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url)
            self.data['users'] = Users(json.loads(user_json)['users'])
            return self.users

        return super(Group, self).__getattr__(key)
