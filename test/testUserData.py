"""Test Skytap Environments API access."""
import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Environments import Environments  # nopep8


class TestUserData(unittest.TestCase):

    """Unittest class to test the the user_data field of VMs and envs."""

    def setUp(self):
        """Build the environment set we want to test with.

        This can generate a lot of API calls, so in the typical case, it's
        better not to "check all". Set vms_to_check to the limit to count.
        """
        self.environments = Environments()
        self.vms_to_check = 10

    def test_basic_userdata(self):
        """Run some simple checks of UserData."""
        vm_count = 0
        for e in self.environments:
            self.check_userdata(e)
            for v in e.vms:
                if vm_count > self.vms_to_check:
                    return
                vm_count += 1
                self.check_userdata(v)

    def check_userdata(self, parent):
        """Check one environment or VM userdata element and object."""
        self.assertTrue(str(parent.user_data) == str(parent.user_data.contents), 'ID ' + str(parent.id) + ': Userdata mismatch.')
        self.assertTrue(parent.user_data.id == 0)
