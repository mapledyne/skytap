from skytap.models.SkytapResource import SkytapResource
from skytap.Users import Users
import json


class Project(SkytapResource):
    def __init__(self, project_json):
        super(Project, self).__init__(project_json)

    def _calculate_custom_data(self):
        self.users = Users(self.users)
        for user in self.users:
            if user.url == self.owner_url:
                self.owner_name = user.name
                break
