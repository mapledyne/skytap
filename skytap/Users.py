from functools import wraps
import json
from skytap.framework.ApiClient import ApiClient
from skytap.models.User import User


class Users(ApiClient):
    def __init__(self):
        ApiClient.__init__(self)
        self.user_list = {}

    def check_user_list(self):
        if (len(self.user_list) == 0):
            users_list_json = json.loads(self.rest('/users'))
            for j in users_list_json:
                self.user_list[int(j['id'])] = User(j)

    def __len__(self):
        self.check_user_list()
        return len(self.user_list)

    def __str__(self):
        all_users = ''
        for u in self.user_list:
            all_users += str(self.user_list[u]) + '\n'
        return all_users

    def __getitem__(self, key):
        return self.user_list[key]

    def __iter__(self):
        return iter(self.user_list)

    def next(self):
        return next(self.user_list)
