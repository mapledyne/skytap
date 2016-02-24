"""Skytap API object wrapping Skytap users.

This roughly translates to the Skytap API call of /v2/users REST call,
but gives us better access to the bits and pieces of the user.

If accessed via the command line (``python -m skytap.Users()``) this will
return the quotas from Skytap in a JSON format.
"""
import json
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.User import User


class Users(SkytapGroup):

    """Set of Skytap users.

    :Example:
    >>> u = Users()
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

    def in_region(self, region):
        """Count the number of users in a region."""
        count = 0
        for u in self.data:
            if self[u].default_region == region:
                count += 1
        return count

    def admins(self):
        """Count the numbers of admins."""
        count = 0
        for u in self.data:
            if self[u].admin:
                count += 1
        return count

if __name__ == '__main__':
    users = Users()
    print(json.dumps(users.json, indent=4))
