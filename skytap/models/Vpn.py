import json
from skytap.models.SkytapResource import SkytapResource


class Vpn(SkytapResource):
    def __init__(self, vpn_json):
        super(Vpn, self).__init__(vpn_json)

    def _calculate_custom_data(self):
        self.active = self.status == 'active'
