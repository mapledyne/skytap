import json
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vm import Vm


class Vms(SkytapGroup):
    def __init__(self, vms_json):
        super(Vms, self).__init__()
        self.load_list_from_json(vms_json, Vm)
