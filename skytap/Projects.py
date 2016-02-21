from skytap.models.Project import Project
from skytap.models.SkytapGroup import SkytapGroup
import json


class Projects(SkytapGroup):
    def __init__(self):
        super(Projects, self).__init__()
        self.load_list_from_api('/v2/projects', Project)

if __name__ == '__main__':
    projects = Projects()
    print json.dumps(projects.json, indent=4)
