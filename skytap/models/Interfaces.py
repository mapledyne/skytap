"""Support for Skytap interfacess."""
import json

from skytap.framework.ApiClient import ApiClient  # noqa
from skytap.models.Interface import Interface  # noqa
from skytap.models.PublishedServices import PublishedServices  # noqa
from skytap.models.SkytapGroup import SkytapGroup  # noqa


class Interfaces(SkytapGroup):
    """A list of Interfaces."""

    def __init__(self, interface_json, vm_url):
        """Create the list of Interfaces.

        Args:
            interfaces_json (string): The JSON from Skytap API to build the list
                                      from.
        """
        super(Interfaces, self).__init__()
        self.load_list_from_json(interface_json, Interface)
        for i in self.data:
            self.data[i].data['url'] = (vm_url + "/interfaces/"
                                        "" + self.data[i].id)

            api = ApiClient()
            services_json = json.loads(api.rest(self.data[i].url))
            self.data[i].services = PublishedServices(services_json["services"],
                                                      self.data[i].url)
