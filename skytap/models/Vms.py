"""Support for Skytap VMs."""
import json
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vm import Vm


class Vms(SkytapGroup):

    """A list of VMs."""

    def __init__(self, vms_json, env):
        """Create the list of VMs.

        :param vms_json: The JSON from Skytap API to build the list from.
        :type vms_json: json
        :param parent: The parent object - evironment or template.
        :type parent: Environment or template

        """
        super(Vms, self).__init__()
        self.load_list_from_json(vms_json, Vm)
        for v in self.data:
            self.data[v].data['url'] = ('/v2/configurations/' + str(env) +
                                        '/vms/' + str(self.data[v].id))
