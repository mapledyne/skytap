import json
from skytap.models.Quota import Quota
from skytap.models.SkytapGroup import SkytapGroup


class Quotas(SkytapGroup):
    def __init__(self):
        super(Quotas, self).__init__()
        self.load_list_from_api('/v2/company/quotas', Quota)

if __name__ == '__main__':
    quotas = Quotas()
    print(json.dumps(quotas.json, indent=4))

    print str(quotas)
