"""Skytap API object wrapping Skytap groups.

This roughly translates to the Skytap API call of /v2/groups REST call,
but gives us better access to the bits and pieces of the group.

If accessed via the command line (``python -m skytap.Groups``) this will
return the groups from Skytap in a JSON format.
"""
import json
import logging
from skytap.framework.ApiClient import ApiClient
from skytap.models.Group import Group
from skytap.models.SkytapGroup import SkytapGroup
import sys


class Groups(SkytapGroup):

    """Set of Skytap groups.

    Example:
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

    def add(self, group, description=''):
        """Add one group.

        Args:
            group (str): The group name to add.
            description (str): The group description to add.

        Returns:
            int: The new group id from Skytap.

        Example:
            >>> groups = skytap.Groups()
            >>> new_group = groups.add('muppets', 'felt covered friends')
            >>> print(groups[new_group].name)
        """
        logging.info('Adding group: ' + group)
        api = ApiClient()
        data = {"name": group,
                "description": description}
        url = self.url + '.json'
        response = api.rest(url, data, 'POST')
        new_group = json.loads(response)
        self.refresh()
        if 'id' in new_group:
            return int(new_group['id'])
        logging.warning('Trying to create group (' + group + '), but ' +
                        'got an unexpected return from Skytap. Response:\n' +
                        response)
        return 0

    def delete(self, group):
        """Delete a group.

        .. warning::
            This is unrecoverable. Use with caution.

        Args:
            group (Group): The group to delete.

        Returns:
            bool: True if group deleted.

        Raises:
            TypeError: if group is not a Group
        """
        if isinstance(group, int):
            if group not in self.data:
                raise KeyError
            group = self.data[group]
        if not isinstance(group, Group):
            raise KeyError

        target_id = group.id

        group.delete()
        self.refresh()

        return target_id not in self.data

if __name__ == '__main__':
    print(Groups().main(sys.argv[1:]))
