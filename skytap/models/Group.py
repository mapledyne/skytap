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

    def add_user(self, user):
        """Add a :class:`User` to the group.

        Args:
            user (int): id of the user to add.

        Raises:
            TypeError: If user is not an :class:`int`.
            KeyError: If user is not in :class:`Users` list.
        Returns:
            bool: True if the user was added.

        Example:
            >>> groups = skytap.Groups()
            >>> users = skytap.Users()
            >>> for u in users:
            ...     groups[12345].add(u.id)
        """
        if (type(user) is not int):
            raise TypeError('User must be an int.')
        if (user not in Users()):
            raise KeyError('User to add not found.')

        api = ApiClient()
        user_json = api.rest(self.url + '/users/' + str(user) + '.json',
                             {},
                             'PUT')
        self.refresh()
        return user in self.data
