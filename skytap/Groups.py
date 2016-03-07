"""Skytap API object wrapping Skytap Groups.

This roughly translates to the Skytap API call of /v2/groups REST call,
but gives us better access to the bits and pieces of the groups.

**Accessing via command line**

If accessed via the command line this will return the environments from
Skytap in a JSON format::

    python -m skytap.Groups

If you know the environment you want information on, you can also specify
it directly. You can search by id or by a part of the environment name::

    python -m skytap.Groups 12345
    python -m skytap.Groups test


**Accessing via Python**

You can access the Skytap environments by the :class:`skytap.Groups` object.

Example:

.. code-block:: python

    groups = skytap.Groups()
    for g in groups:
        print(g.name)

Each group has many things you can do with it - see the
:class:`skytap.models.Group` object for actions you can take on an
individual group.

On the full list of groups, you can also do a few other things:

    - :func:`add`: add a new group.
    - :func:`delete`: delete a group.

Environments can also perform any of the actions of other
:class:`SkytapGroup` objects. See the documentation
on the :class:`skytap.models.SkytapGroup` class for
information there.
"""
import json
import sys

from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.Group import Group
from skytap.models.SkytapGroup import SkytapGroup


class Groups(SkytapGroup):

    """Set of Skytap groups.

    Generally, access this through simply creating a
    :class:`skytap.Groups` object.

    Example:

    .. code-block:: python

        groups = skytap.Groups()
        for g in groups:
            print(g.name)
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

        .. code-block:: python

            groups = skytap.Groups()
            new_group = groups.add('muppets', 'felt covered friends')
            print(groups[new_group].name)
        """
        Utils.info('Adding group: ' + group)
        api = ApiClient()
        data = {"name": group,
                "description": description}
        url = self.url + '.json'
        response = api.rest(url, data, 'POST')
        new_group = json.loads(response)
        self.refresh()
        if 'id' in new_group:
            return int(new_group['id'])
        Utils.warning('Trying to create group (' + group + '), but ' +
                      'got an unexpected return from Skytap. Response:\n' +
                      response)
        return 0

    def delete(self, group):
        """Delete a group.

        .. warning::
            This is unrecoverable. Use with caution.

        Args:
            group: The :class:`~skytap.models.Group` to delete.

        Returns:
            bool: True if group deleted.

        Raises:
            TypeError: if group is not a :class:`~skytap.models.Group`
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
