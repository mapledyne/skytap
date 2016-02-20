from skytap.models.Project import Project
from skytap.models.SkytapGroup import SkytapGroup

class Projects(SkytapGroup):
    def __init__(self):
        super(Projects, self).__init__()
        self.load_list_from_api('/v2/projects', Project)

    def count_in_region(self, region):
        count = 0
        for u in self.data:
            if self[u].default_region == region:
                count += 1
        return count
