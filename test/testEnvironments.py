"""Test Skytap Environments API access."""
import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Environments import Environments  # nopep8


class TestEnvironments(unittest.TestCase):

    """Unittest class to test the Environments."""

    def setUp(self):
        """Build the environment set we want to test with."""
        self.environments = Environments()

    def test_basic_environment_check(self):
        """Run tests on the environment list as a whole."""
        self.assertTrue(len(self.environments) > 0,
                        'Environment list is empty.')
        self.assertTrue(self.environments.svms > 0)
        self.assertTrue(self.environments.vm_count > 0)
        self.assertTrue(self.environments.svms > self.environments.vm_count,
                        'SVM count should never be more than VM count.')

        # Iterate over the list.
        for e in self.environments:
            self.environment_check(e)

    def environment_check(self, env):
        """Run tests on an individual environment."""
        self.assertTrue(env.id > 0, 'No environment ID found')
        self.assertTrue(len(env.details()) > 0,
                        env.name + ': No details found.')
        self.assertTrue(len(str(env)) > 0,
                        env.name + ': No string conversion found.')
        notes = env.notes
        for n in notes:
            self.assertTrue(len(n.text) > 0,
                            str(env.id) + ": note [" + str(n.id) +
                            "] empty.")
            self.assertTrue(n.created_at <= n.updated_at,
                            str(env.id) + ": note [" + str(n.id) +
                            "] updated before it was created.")

    def test_basic_vm_check(self):
        """Run checks for VMs."""
        for e in self.environments:
            for v in e.vms:
                self.assertTrue(v.id > 0, 'Env ' + str(e.id) + ': No VM id found.')  # nopep8
                self.assertTrue(len(str(v)) > 0, 'VM ' + str(v.id) +
                                ': No string conversion found.')
                self.assertTrue(len(v.url))
                print v.details()
