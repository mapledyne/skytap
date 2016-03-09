"""Support for Skytap services."""
import json

from skytap.models.SkytapGroup import SkytapGroup  # noqa
from skytap.models.PublishedService import PublishedService  # noqa


class PublishedServices(SkytapGroup):
    """A list of Published Services."""

    def __init__(self, service_json, interface_url):
        """Create the list of Published Services.

        Args:
            services_json (string): The JSON from Skytap API to build the list
                                    from.
        """
        super(PublishedServices, self).__init__()
        self.load_list_from_json(service_json, PublishedService)
        for s in self.data:
            self.data[s].data["url"] = (interface_url + "/services/"
                                        "" + str(self.data[s].id))
