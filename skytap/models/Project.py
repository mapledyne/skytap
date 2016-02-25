"""Support for Projects."""
import json
from skytap.models.SkytapResource import SkytapResource
from skytap.Users import Users


class Project(SkytapResource):

    """One Skytap project."""

    def __init__(self, project_json):
        """Build one Skytap project."""
        super(Project, self).__init__(project_json)

    def _calculate_custom_data(self):
        """Make the list of users into a Users list."""
        self.data['users'] = Users(self.users)
        for key in self.users.keys():
            if self.users[key].url == self.owner_url:
                self.owner_name = self.users[key].name
                break
