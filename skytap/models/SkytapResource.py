"""Base class for all Skytap Resources."""
import json
import six
from skytap.framework.ApiClient import ApiClient
from skytap.framework.Json import SkytapJsonEncoder
import skytap.framework.Utils as Utils


class SkytapResource(object):

    """Represents one Skytap Resource - a VM, Environment, User, whatever."""

    def __init__(self, initial_json):
        super(SkytapResource, self).__init__()

        self.data = {}
        self.data["id"] = 0
        for k in initial_json.keys():
            self.data[k] = initial_json[k]
        if 'url' in self.data:
            if '/v2/' in self.url:
                self.url_v1 = self.url.replace('/v2/', '/')
                self.url_v2 = self.url
            else:
                self.url_v1 = self.url
                self.url_v2 = None
        self._convert_data_elements()
        self._calculate_custom_data()

    def _calculate_custom_data(self):
        """Used so objects can create and calculate new data elements."""
        pass

    def _convert_data_elements(self):
        """Convert some data elements into variable types that make sense."""
        if 'created_at' in self.data:
            try:
                self.data['created_at'] = Utils.convert_date(self.created_at)
            except ValueError:
                pass
        if 'updated_at' in self.data:
            try:
                self.data['updated_at'] = Utils.convert_date(self.updated_at)
            except ValueError:
                pass
        if 'last_installed' in self.data:
            try:
                self.data['last_installed'] = Utils.convert_date(self.last_installed)  # nopep8
            except ValueError:
                pass

        try:
            self.data['id'] = int(self.data['id'])
        except ValueError:
            pass

    def refresh(self):
        """Refresh the data in our object, if we have a URL to pull from."""
        if 'url' not in self.data:
            return KeyError
        api = ApiClient()
        env_json = api.rest(self.url)
        self.__init__(json.loads(env_json))

    def __getattr__(self, key):
        if key not in self.data:
            raise AttributeError
        return self.data[key]

    def details(self):
        """Print a simple list of everything the object knows about.

        Useful for debugging, but not intended for much else.
        """
        det = ''
        for x in self.data:
            try:
                det += str(x) + ': ' + str(self.data[x]) + '\n'
            except UnicodeEncodeError:
                det += (unicode(x).encode('utf_8') +
                        ': ' + unicode(self.data[x]).encode('utf_8') +
                        '\n')
        return det

    def json(self):
        """Convert the object to JSON."""
        return json.dumps(self.data, indent=4, cls=SkytapJsonEncoder)

    def __str__(self):
        return self.name

    def __int__(self):
        return int(self.id)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __hash__(self):
        return hash(repr(self.data))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __contains__(self, key):
        return key in self.data
