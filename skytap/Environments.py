from skytap.models.Environment import Environment
from skytap.models.SkytapGroup import SkytapGroup

class Environments(SkytapGroup):
    def __init__(self):
        super(Environments, self).__init__()
        self.load_list_from_api('/v2/configurations', Environment)

    def vm_count(self):
        count = 0
        for e in self.data:
            count += self.data[e].vm_count
        return count

    def svms(self):
        count = 0
        for e in self.data:
            count += self.data[e].svms
        return count
