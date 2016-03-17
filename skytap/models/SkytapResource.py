"""Base class for all Skytap Resources."""
import json

from skytap.framework.ApiClient import ApiClient  # noqa
from skytap.framework.Json import SkytapJsonEncoder  # noqa
import skytap.framework.Utils as Utils  # noqa


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

    def _convert_data_elements(self):
        """Convert some data elements into variable types that make sense."""

        try:
            self.data['created_at'] = Utils.convert_date(self.data['created_at'])  # noqa
        except (ValueError, AttributeError, KeyError):
            pass

        try:
            self.data['last_login'] = Utils.convert_date(self.data['last_login'])  # noqa
        except (ValueError, AttributeError, KeyError):
            pass

        try:
            self.data['last_run'] = Utils.convert_date(self.data['last_run'])
        except (ValueError, AttributeError, KeyError):
            pass

        try:
            self.data['updated_at'] = Utils.convert_date(self.data['updated_at'])  # noqa
        except (ValueError, AttributeError, KeyError):
            pass
        try:
            self.data['last_installed'] = Utils.convert_date(self.data['last_installed'])  # noqa
        except (ValueError, AttributeError, KeyError):
            pass

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
        if key not in self.data:
            raise AttributeError
        return self.data[key]

    def json(self):
        """Convert the object to JSON."""
        return json.dumps(self.data, indent=4, cls=SkytapJsonEncoder)

    def __str__(self):
        return str(self.name)

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
