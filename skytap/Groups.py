"""Skytap API object wrapping Skytap groups.

This roughly translates to the Skytap API call of /v2/groups REST call,
but gives us better access to the bits and pieces of the group.

If accessed via the command line (``python -m skytap.Groups``) this will
return the groups from Skytap in a JSON format.
"""
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Group import Group
import sys


class Groups(SkytapGroup):

    """Set of Skytap groups.

    :Example:
    >>> g = skytap.Groups()
    >>> print len(g)
    12
    """

    def __init__(self, json_list=None):
        """Build an initial list of groups.

        If the first parameter is missing, go to the API to get the full list.
        """
        super(Groups, self).__init__()
        if json_list is None:
            self.load_list_from_api('/v2/groups', Group)
        else:
            self.load_list_from_json(json_list, Group)


if __name__ == '__main__':
    print(Groups().main(sys.argv))
