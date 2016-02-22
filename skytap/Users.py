from skytap.models.User import User
from skytap.models.SkytapGroup import SkytapGroup
import json


class Users(SkytapGroup):
    def __init__(self, json_list=None):
        super(Users, self).__init__()
        if json_list is None:
            self.load_list_from_api('/v2/users', User)
        else:
            self.load_list_from_json(json_list, User)

    def in_region(self, region):
        count = 0
        for u in self.data:
            if self[u].default_region == region:
                count += 1
        return count

    def admins(self):
        count = 0
        for u in self.data:
            if self[u].admin:
                count += 1
        return count

if __name__ == '__main__':
    users = Users()
    print(json.dumps(users.json, indent=4))
