import json
import os
import sys

sys.path.append('..')
from skytap.Users import Users  # nopep8


class TestUsers(object):

    def setUp(self):
        self.users = Users()

    def test_basic_user_check(self):
        assert len(self.users) > 0, 'User list is empty.'

        for u in self.users:
            self.user_check(u)

        assert self.users.admins() > 0

    def user_check(self, user):
        assert user.id > 0, 'No user ID found'
        assert len(user.details()) > 0, user.name + ': No details found.'
        assert len(str(user)) > 0, user.name + ': No string conversion found.'
