import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Users import Users  # nopep8


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.users = Users()

    def test_basic_user_check(self):
        self.assertTrue(len(self.users) > 0,
                        'User list is empty.')

        for u in self.users:
            self.user_check(u)

        self.assertTrue(self.users.admins() > 0)

    def user_check(self, user):
        self.assertTrue(user.id > 0, 'No user ID found')
        self.assertTrue(len(user.details()) > 0,
                        user.name + ': No details found.')
        self.assertTrue(len(str(user)) > 0,
                        user.name + ': No string conversion found.')
