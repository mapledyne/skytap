import json
from skytap.models.SkytapResource import SkytapResource


class User(SkytapResource):
    def __init__(self, user_json):
        super(User, self).__init__(user_json)

    def _calculate_custom_data(self):
        self.data['name'] = self.first_name + ' ' + self.last_name
        if 'account_role' in self.data:
            self.data['admin'] = self.account_role == 'admin'
