import json
from skytap.framework.ApiClient import ApiClient
from skytap.models.SkytapResource import SkytapResource


class User(SkytapResource):
    def __init__(self, user_json):
        super(User, self).__init__(user_json)

    def _calculate_custom_data(self):
        if 'sso_enabled' in self.data:
            self.data['sso'] = bool(self.sso_enabled)
        else:
            self.data['sso'] = False

        self.data['name'] = self.first_name + ' ' + self.last_name
        if 'account_role' in self.data:
            self.data['admin'] = self.account_role == 'admin'
        if 'configurations' in self.data:
            if (isinstance(self.data['configurations'], list)):
                if len(self.data['configurations']) > 0:
                    if isinstance(self.data['configurations'][0], dict):
                        self.data['configurations'] = Environments(self.data['configurations'])  # nopep8

    def delete(self, transfer_user):
        """Delete the user."""
        if isinstance(transfer_user, User):
            transfer_user = transfer_user.id
        if not isinstance(transfer_user, int):
            raise TypeError('transfer_user must be a User or int.')
        logging.info('Deleting user: ' +
                     str(self.id) + ' (' + self.name + ') and transferring ' +
                     'resources to user id: ' + str(transfer_user))
        api = ApiClient()

        transfer = {"transfer_user_id": str(transfer_user)}

        response = api.rest(self.url,
                            transfer,
                            'DELETE')
        return response
