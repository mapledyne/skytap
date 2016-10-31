"""Support for Skytap services."""
from skytap.models.PublishedService import PublishedService  # noqa
from skytap.models.SkytapGroup import SkytapGroup  # noqa


class PublishedServices(SkytapGroup):
    """A list of Published Services."""

    def __init__(self, service_json, interface_url):
        """Create the list of Published Services.

        Args:
            services_json (string): The JSON from Skytap API to build the list
                                    from.
        """
        super(PublishedServices, self).__init__()
        self.load_list_from_json(service_json, PublishedService, interface_url)
        for service in self.data:
            self.data[service].data["url"] = (interface_url + "/services/"
                                              "" + str(self.data[service].id))
