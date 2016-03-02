"""Base object to handle groups of Skytap objects."""
from collections import Iterator
import json
import six
from skytap.framework.ApiClient import ApiClient
from skytap.framework.Json import SkytapJsonEncoder
import skytap.framework.Utils as Utils


class SkytapGroup(ApiClient, six.Iterator):

    """Base object for use with Skytap resource groups."""

    def __init__(self):
        super(SkytapGroup, self).__init__()
        self.data = {}
        self.itercount = 0
        self.search_fields = ['name']



    def load_list_from_api(self, url, target, params={}):
        """Load something from the Skytap API and fill this object.

        .. note: This should rarely be called by anything but a child object,
            typically in its __init__() method.

        Args:
            url (str): The Skytap URL to load ('/v2/users').
            target (SkytapResource): The resource type to load ('User')
            params (dict): Any URL parameters to add to URL.

        This should look like, in the child object::

            self.load_list_from_api('/v2/projects', Project)

        """
        self.load_list_from_json(self.rest(url, params), target)
        self.params = params
        self.url = url
        if '/v2/' in self.url:
            self.url_v1 = self.url.replace('/v2/', '/')
            self.url_v2 = self.url
        else:
            self.url_v1 = self.url
            self.url_v2 = None

    def load_list_from_json(self, json_list, target):
        """Load items from a json list and fill this object.

        Args:
            json_list (list): The list to load the items from.
            target (SkytapResource): The resource type to load ('User')

        This should look like, in the child object::

            self.load_list_from_json(json, Project)

        """
        self.data = {}
        self.target = target

        if isinstance(json_list, str):
            self.json_from_load = json.loads(json_list)
        elif isinstance(json_list, list):
            self.json_from_load = json_list
        else:
            raise TypeError
        for j in self.json_from_load:
            # prefer an int for the ID since that's the most common and
            # easiest to work with, but some things (quotas) have string
            # ids, so we want to leave those alone. A given resource/group
            # will have to handle non-int keys differently if there's a
            # case where that's a problem.
            try:
                self.data[int(j['id'])] = target(j)
            except ValueError:
                self.data[j['id']] = target(j)

    def first(self):
        """Return the first record in the list.

        Mainly used to get a single arbitrary object for testing.

        .. note: The selection of this list depends on how the objects
            are returned from Skytap. This ordering should be considered
            arbitrary and not reliable from one run to the next.

        Returns:
            SkytapResource: An object from the list.
        """
        return self.data[list(self.data)[0]]

    def find(self, search):
        """Return a list of objects, based on the search criteria.

        This looks for matching ids if the search is a number, or searches
        the name if search is a string.

        Args:
            search (int or str): What to search for.
        Returns:
            List: Any environments matching the search criteria.

        Example:
            >>> envs = skytap.Environments().search('testing')

        """
        found = []
        for one in list(self.data):
            test = self.data[one]
            try:
                if int(search) == test.id:
                    found.append(test)
            except ValueError:
                pass
            for field in self.search_fields:
                if str(search).upper() in test.data[field].upper():
                    found.append(test)
        return found

    def refresh(self):
        """Reload our data."""
        self.load_list_from_api(self.url,
                                self.target,
                                self.params)

    def main(self, argv):
        """What to do when called from the command line.

        This function is usually accessed via the command line::

            python -m skytap.Environments

        but can be used to return quick sets of formatted JSON::

            >>> print(skytap.Environments().main())

        Anything passed to the function will be searched for::

            python -m skytap.Users fozzy

        and::

            >>> print(skytap.Users().main('scooter'))

        Args:
            argv (list): Command line arguments

        Returns:
            str: Formatted JSON of the request.
        """
        obj_type = type(self.data[list(self.data)[0]])
        obj_name = obj_type.__name__
        obj_id_type = type(self.data[list(self.data)[0]].id)

        if len(argv) > 0:
            found = self.find(argv[0])
            json_return = []
            for item in found:
                json_return.append(json.loads(item.json()))
            return json.dumps(json_return, indent=4)

        return json.dumps(self.json(), indent=4)

    def json(self):
        """Convert our list into a json."""
        json_return = []
        for item in self.data:
            json_return.append(json.loads(self.data[item].json()))
        return json_return

    def __len__(self):
        return len(self.data)

    def __str__(self):
        data_str = ''
        for u in self.data:
            try:
                data_str += str(self.data[u]) + '\n'
            except UnicodeEncodeError:
                data_str += (unicode(self.data[u]).encode('utf_8') + '\n')
        return data_str

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return self

    def __next__(self):
        if self.itercount >= len(self.data):
            raise StopIteration
        n = list(self.data)[self.itercount]
        self.itercount += 1
        return self.data[n]

    def keys(self):
        """Return the keys from the group list."""
        return self.data.keys()

    def __contains__(self, key):
        return key in self.data
