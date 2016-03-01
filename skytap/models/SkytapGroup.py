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

    def load_list_from_api(self, url, target, params={}):
        """Load something from the Skytap API and fill this object.

        :param url: The Skytap URL to load ('/v2/users').
        :type url: str
        :param target: The resource type to load ('User')
        :type target: SkytapResource
        :param params: Any URL parameters to add to URL.
        :type url: dict

        This should look like, in the child object:
        >>> self.load_list_from_api('/v2/projects', Project)
        """
        self.load_list_from_json(self.rest(url, params), target)
        self.params = params
        self.url = url

    def load_list_from_json(self, json_list, target):
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
        """
        return self.data[list(self.data)[0]]

    def refresh(self):
        """Reload our data."""
        self.load_list_from_api(self.url,
                                self.target,
                                self.params)

    def main(self, argv):
        """What to do when called from the command line."""
        obj_type = type(self.data[list(self.data)[0]])
        obj_name = obj_type.__name__
        obj_id_type = type(self.data[list(self.data)[0]].id)

        if len(argv) > 0:
            try:
                thing = obj_id_type(argv[0])
            except ValueError:
                return Utils.error(obj_name + ' ID not valid.')
            if thing in self.data:
                return self[thing].json()
            else:
                return Utils.error('No ' + obj_name + ' with that ID found.')

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
        return self.data.keys()

    def __contains__(self, key):
        return key in self.data
