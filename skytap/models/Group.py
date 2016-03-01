"""Support for Skytap groups."""
import json
import logging
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

    def _calculate_custom_data(self):
        if 'users' in self.data:
            if (isinstance(self.data['users'], list)):
                if len(self.data['users']) > 0:
                    if isinstance(self.data['users'][0], dict):
                        self.data['users'] = Users(self.data['users'])

    def remove_user(self, user):
        """Remove a :class:`user` from the group.

        Args:
            user (int): id of the user to remove.

        Raises:
            TypeError: If user is not an :class:`int`.
            KeyError: If user is not in :class:`Users` list.

        Returns:
            bool: True if the user was removed.

        Example:
            >>> groups = skytap.Groups()
            >>> groups[1234].remove_user(12345)
        """
        if (type(user) is not int):
            raise TypeError('User must be an int.')

        logging.info('Removing user ' + str(user) +
                     ' from group: ' + self.name)
        api = ApiClient()
        user_json = api.rest(self.url + '/users/' + str(user),
                             {},
                             'DELETE')

        self.refresh()
        return user not in self.users

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

        logging.info('Adding user ' + str(user) + ' to group: ' + self.name)
        api = ApiClient()
        user_json = api.rest(self.url + '/users/' + str(user) + '.json',
                             {},
                             'PUT')
        self.refresh()
        return user in self.users

    def delete(self):
        """Delete the group."""
        logging.info('Deleting group: ' +
                     str(self.id) + ' (' + self.name + ')')
        api = ApiClient()
        response = api.rest(self.url_v1,
                            {},
                            'DELETE')
        return response
