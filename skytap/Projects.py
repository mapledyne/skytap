from skytap.models.Project import Project
from skytap.models.SkytapGroup import SkytapGroup
import sys


class Projects(SkytapGroup):
    def __init__(self):
        super(Projects, self).__init__()
        self.load_list_from_api('/v2/projects', Project)

if __name__ == '__main__':
    print(Projects().main(sys.argv[1:]))
