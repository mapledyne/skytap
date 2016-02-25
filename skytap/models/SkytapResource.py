"""Base class for all Skytap Resources."""
import json
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils


class SkytapResource(object):

    """Represents one Skytap Resource - a VM, Environment, User, whatever."""

    def __init__(self, initial_json):
        """Build one Skytap Resource."""
        super(SkytapResource, self).__init__()

        self.data = {}
        self.data["id"] = 0
        for k in initial_json.keys():
            self.data[k] = initial_json[k]
        # Do some simple date conversion if the data is here.
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
        try:
            self.data['id'] = int(self.data['id'])
        except ValueError:
            pass

        self._calculate_custom_data()

    def refresh(self):
        """Refresh the data in our object, if we have a URL to pull from."""
        if 'url' not in self.data:
            return KeyError
        api = ApiClient()
        env_json = api.rest(self.url)
        self.__init__(json.loads(env_json))

    def _calculate_custom_data(self):
        pass

    def __getattr__(self, key):
        """Make the values accessible.

        This allows all user values to be available via calls like:
        user.id
        """
        if key not in self.data:
            raise AttributeError
        return self.data[key]

    def details(self):
        """Print a simple list of everything the object knows about.

        Useful for debugging, but not intended for much else.
        """
        det = ''
        for x in self.data:
            det += str(x) + ": " + str(self.data[x]) + '\n'
        return det

    def json(self):
        """Convert the object to JSON."""
        return json.dumps(self.data, indent=4)

    def __str__(self):
        """Build string conversion."""
        return '[' + str(self.id) + '] ' + self.name

    def __int__(self):
        """Return id of object."""
        return int(self.id)

    def __gt__(self, other):
        """Handle greater-than requests."""
        return int(self) > int(other)

    def __lt__(self, other):
        """Handle less-than requests."""
        return int(self) < int(other)

    def __hash__(self):
        """Build a simple hash."""
        return hash(self.data)

    def __eq__(self, other):
        """Compare objects."""
        return hash(self) == hash(other)

    def __contains__(self, key):
        """Return true if resource have a given value."""
        return key in self.data
