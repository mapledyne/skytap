"""Skytap API object wrapping Skytap users.

This roughly translates to the Skytap API call of /v2/users REST call,
but gives us better access to the bits and pieces of the user.

If accessed via the command line (``python -m skytap.Users``) this will
return the users from Skytap in a JSON format.
"""
import json
import logging
from skytap.framework.ApiClient import ApiClient
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.User import User
import sys


class Users(SkytapGroup):

    """Set of Skytap users.

    :Example:
    >>> u = skytap.Users()
    >>> print len(u)
    58
    """

    def __init__(self, json_list=None):
        """Build an initial list of users.

        If the first parameter is missing, go to the API to get the full list.
        """
        super(Users, self).__init__()
        if json_list is None:
            self.load_list_from_api('/v2/users', User)
        else:
            self.load_list_from_json(json_list, User)

    def admins(self):
        """Count the numbers of admins."""
        count = 0
        for u in self.data:
            if self[u].admin:
                count += 1
        return count

    def add(self, login_name, email=None):
        """Add one user.

        Args:
            login_name (str): The login id of the account, usually an email.
            email (str): The email of the account. If blank, will use
                login_name.

        Returns:
            int: The new user id from Skytap.

        Example:
            >>> users = skytap.Users()
            >>> new_user = users.add('kermit.frog@fulcrum.net')
            >>> print(users[new_user].login_name)
        """
        logging.info('Adding user: ' + login_name)
        if email is None:
            email = login_name
        api = ApiClient()
        data = {"login_name": login_name,
                "email": email}
        url = self.url_v1 + '.json'
        response = api.rest(url, data, 'POST')
        new_group = json.loads(response)
        self.refresh()
        if 'id' in new_group:
            return int(new_group['id'])
        logging.warning('Trying to create group (' + group + '), but ' +
                        'got an unexpected return from Skytap. Response:\n' +
                        response)
        return 0

    def delete(self, user, transfer_user):
        """Delete a user.

        .. warning::
            This is unrecoverable. Use with caution.

        Args:
            user (User or int): The user to delete.
            transfer_user (User or int): Transfer all assets to this user.

        Returns:
            bool: True if user deleted.

        Raises:
            TypeError: if user or transfer_user is not a User or int.
            KeyError: If user or transfer_user isn't a user in the Users list.
        """
        if isinstance(user, int):
            if user not in self.data:
                raise KeyError
            user = self.data[user]
        if not isinstance(user, User):
            raise KeyError

        if isinstance(transfer_user, int):
            if transfer_user not in self.data:
                raise KeyError
            transfer_user = self.data[transfer_user]
        if not isinstance(transfer_user, User):
            raise KeyError

        target_id = group.id

        user.delete(tranfer_user)
        self.refresh()

        return target_id not in self.data

if __name__ == '__main__':
    print(Users().main(sys.argv[1:]))
