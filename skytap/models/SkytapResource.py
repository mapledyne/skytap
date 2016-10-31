"""Base class for all Skytap Resources."""
import json

from skytap.framework.ApiClient import ApiClient  # noqa
from skytap.framework.Json import SkytapJsonEncoder  # noqa
import skytap.framework.Utils as Utils  # noqa


class SkytapResource(object):
    """Represents one Skytap Resource - a VM, Environment, User, whatever."""

    def __init__(self, initial_json):
        """Build one SkytapResource thing."""
        super(SkytapResource, self).__init__()

        self.data = {}
        self.data["id"] = 0
        for k in initial_json.keys():
            self.data[k] = initial_json[k]
        if 'url' in self.data:
            if '/v2/' in self.url:
                self.data['url_v1'] = self.url.replace('/v2/', '/')
                self.data['url_v2'] = self.url
            else:
                self.data['url_v1'] = self.url
                self.data['url_v2'] = None
        self._convert_data_elements()
        self._calculate_custom_data()

    def _calculate_custom_data(self):
        """Used so objects can create and calculate new data elements."""
        pass

    def _convert_date(self, element):
        """Try to convert element to a date."""
        try:
            self.data[element] = Utils.convert_date(self.data[element])
        except (ValueError, AttributeError, KeyError):
            pass

    def _convert_data_elements(self):
        """Convert some data elements into variable types that make sense."""
        self._convert_date('created_at')
        self._convert_date('last_login')
        self._convert_date('last_run')
        self._convert_date('updated_at')
        self._convert_date('last_installed')

        try:
            self.data['id'] = int(self.data['id'])
        except (ValueError, AttributeError, KeyError):
            pass

    def refresh(self):
        """Refresh the data in our object, if we have a URL to pull from."""
        if 'url' not in self.data:
            return KeyError
        api = ApiClient()
        env_json = api.rest(self.url)
        self.__init__(json.loads(env_json))

    def __getattr__(self, key):
        """Access custom attributes.

        This allows us to access members of self.data as if they're attributes
        of the resource. This transparently extends the object with all of the
        keys returned from the Skytap API without each resource having to do
        anything special except for exception cases.
        """
        if key not in self.data:
            raise AttributeError
        return self.data[key]

    def json(self):
        """Convert the object to JSON."""
        return json.dumps(self.data, indent=4, cls=SkytapJsonEncoder)

    def __str__(self):
        """Represent the resource as a string."""
        return str(self.name)

    def __int__(self):
        """Represent the resource as an int."""
        return int(self.id)

    def __gt__(self, other):
        """Compare the resource to another one, helpful for sorting."""
        return int(self) > int(other)

    def __lt__(self, other):
        """Compare the resource to another one, helpful for sorting."""
        return int(self) < int(other)

    def __hash__(self):
        """Represent the resource as a hash."""
        return hash(repr(self.data))

    def __eq__(self, other):
        """Compare the resource to another one, helpful for sorting."""
        return hash(self) == hash(other)

    def __contains__(self, key):
        """Check if this resource has a particular key in its data."""
        return key in self.data
