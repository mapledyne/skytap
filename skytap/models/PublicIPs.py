"""Support for Skytap services."""
from skytap.models.PublicIP import PublicIP  # noqa
from skytap.models.SkytapGroup import SkytapGroup  # noqa


class PublicIPs(SkytapGroup):
    """A list of Public IPs."""

    def __init__(self, service_json, interface_url):
        """Create the list of Public IPs.

        Args:
            services_json (string): The JSON from Skytap API to build the list
                                    from.
        """
        super(PublicIPs, self).__init__()
        self.load_list_from_json(service_json, PublicIP, interface_url)
        for service in self.data:
            self.data[service].data["url"] = (interface_url + "/v2/ips/"
                                              "" + str(self.data[service].id))
