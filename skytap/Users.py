"""Skytap API object wrapping Skytap users.

This roughly translates to the Skytap API call of /v2/users REST call,
but gives us better access to the bits and pieces of the user.

If accessed via the command line (``python -m skytap.Users()``) this will
return the quotas from Skytap in a JSON format.
"""
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

if __name__ == '__main__':
    Users().main(sys.argv)
