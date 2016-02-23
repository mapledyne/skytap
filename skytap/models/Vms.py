import json
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vm import Vm


class Vms(SkytapGroup):
    def __init__(self, vms_json, env):
        super(Vms, self).__init__()
        self.load_list_from_json(vms_json, Vm)
        for v in self.data:
            self.data[v].data['url'] = '/v2/configurations/' + env + '/vms/' + str(self.data[v].id)
