from skytap.models.Vpn import Vpn
from skytap.models.SkytapGroup import SkytapGroup
import json


class Vpns(SkytapGroup):
    def __init__(self):
        super(Vpns, self).__init__()
        self.load_list_from_api('/v2/vpns', Vpn)

if __name__ == '__main__':
    vpns = Vpns()
    print json.dumps(vpns.json, indent=4)
