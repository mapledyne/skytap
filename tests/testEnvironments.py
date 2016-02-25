"""Test Skytap Environments API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # nopep8


class TestEnvironments(object):

    """Unittest class to test the Environments."""

    def setUp(self):
        """Build the environment set we want to test with."""
        self.environments = Environments()

    def test_do_some_environments_exist(self):
        """Check to see if we have some environments returned."""
        assert len(self.environments) > 0

    def test_svm_count(self):
        """Ensure our SVMs over 0."""
        assert self.environments.svms() > 0

    def test_vm_count(self):
        """Ensure our VMs over 0."""
        assert self.environments.vm_count() > 0

    def test_svm_vs_vm_count(self):
        """Make sure svm count is greater than vm count."""
        assert self.environments.svms() >= self.environments.vm_count()

    def test_environment_set(self):
        """Run tests over the individual environments."""
        for e in self.environments:
            self.environment_check(e)

    def environment_check(self, env):
        """Run tests on an individual environment."""
        assert env.id > 0, 'No environment ID found'
        assert len(env.details()) > 0, env.name + ': No details found.'
        assert len(str(env)) > 0, env.name + ': No string conversion found.'
