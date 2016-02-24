import json
from skytap.models.Environment import Environment
from skytap.models.SkytapGroup import SkytapGroup


class Environments(SkytapGroup):
    def __init__(self):
        super(Environments, self).__init__()
        self.load_list_from_api('/v2/configurations',
                                Environment,
                                {'scope': 'company'})

    def vm_count(self):
        """Count the total number of VMs."""
        count = 0
        for e in self.data:
            count += self.data[e].vm_count
        return count

    def svms(self):
        """Count the total number of SVMs in use."""
        count = 0
        for e in self.data:
            count += self.data[e].svms
        return count

    def storage(self):
        """Count the total amount of storage in use."""
        count = 0
        for e in self.data:
            count += self.data[e].storage
        return count

if __name__ == '__main__':
    envs = Environments()
    print(json.dumps(envs.json, indent=4))
