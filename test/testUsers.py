import json
import os
import sys
import unittest
import random

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

        # Get a random user to get this and do ... something with it to check.
        one_user = self.users[random.choice(list(self.users.keys()))]
        print one_user.details()

        # Assert if 0:
        print "US-West: " + str(self.users.count_in_region("US-West"))

        # Assert if 0:
        print "Admin count: " + str(self.users.count_admins())
