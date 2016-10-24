"""Support for an interface resource in Skytap."""
import json

from skytap.framework.ApiClient import ApiClient  # noqa
from skytap.models.PublishedServices import PublishedServices  # noqa
from skytap.models.SkytapResource import SkytapResource  # noqa


class Interface(SkytapResource):
    """One Skytap (network) Interface."""

    def __getattr__(self, key):
        """Get attributes.

        Interfaces aren't fully returned when the API call is made -
        Published Services aren't returned. Often this doesn't matter,
        so we don't automatically pull this information. However, if you ask
        for the services, this function will go and get the requested
        information on demand. This allows saving of API calls (we don't
        request this unless you're accessing Published Services), but also
        you can treat the object as if the services are there all along. We'll
        get the info when you ask for it, and you can move along like it was
        there from the start.

        If you're doing anything other than asking for services, then this
        passes the call upstream to do the default stuff.
        """
        if key == 'services':
            api = ApiClient()
            services_json = json.loads(api.rest(self.url))
            self.services = PublishedServices(services_json["services"],
                                              self.url)
            return self.services

        return super(Interface, self).__getattr__(key)
