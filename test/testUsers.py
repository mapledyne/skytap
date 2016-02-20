import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Users import Users


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.users = Users()

    def test_basic_user_check(self):
        self.assertTrue(len(self.users) > 0,
                        'User list is empty.')
        # Iterate over the list.
        for u in self.users:
            a_user = str(self.users[u])  # test string conversion
        print self.users[115046].details()
