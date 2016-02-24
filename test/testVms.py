"""Test Skytap Environments API access."""
import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Environments import Environments  # nopep8


class TestVms(unittest.TestCase):

    """Unittest class to test the VMs."""

    def setUp(self):
        """Build the environment set we want to test with.

        This can generate a lot of API calls, so we quiet it down with the
        limit set by vms_to_check.
        """
        self.environments = Environments()
        self.vms_to_check = 10

    def test_basic_vm_check(self):
        """Run checks for VMs."""
        for e in self.environments:
            vm_count = 0
            for v in e.vms:
                if vm_count > self.vms_to_check:
                    return
                vm_count += 1
                self.assertTrue(v.id > 0, 'Env ' + str(e.id) + ': No VM id found.')  # nopep8
                self.assertTrue(len(str(v)) > 0, 'VM ' + str(v.id) +
                                ': No string conversion found.')
                self.assertTrue(len(v.url))
