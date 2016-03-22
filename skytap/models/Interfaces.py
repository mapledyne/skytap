"""Support for Skytap interfacess."""
import json

from skytap.models.Interface import Interface  # noqa
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
        self.load_list_from_json(interface_json, Interface, vm_url)
        for i in self.data:
            self.data[i].data['url'] = (vm_url + "/interfaces/"
                                        "" + str(self.data[i].id))
