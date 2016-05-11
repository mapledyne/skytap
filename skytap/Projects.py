"""Support for Skytap API access to projects.

If accessed via the command line (``python -m skytap.Projects``) this will
return the projects from Skytap in a JSON format.
"""

import sys

from skytap.models.Project import Project
from skytap.models.SkytapGroup import SkytapGroup


class Projects(SkytapGroup):
    """Set of Skytap projects.

    Example:

    .. code-block:: python
        p = skytap.Projects()
        print len(p)
    """

    def __init__(self):
        """Initial set of projects."""
        super(Projects, self).__init__()
        self.load_list_from_api('/v2/projects', Project)

if __name__ == '__main__':
    print(Projects().main(sys.argv[1:]))
