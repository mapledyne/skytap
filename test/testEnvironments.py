import json
import os
import sys
import unittest
import random

sys.path.append('..')
from skytap.Environments import Environments

class TestEnvironments(unittest.TestCase):

    def setUp(self):
        self.environments = Environments()

    def test_basic_environment_check(self):
        self.assertTrue(len(self.environments) > 0, 'Environment list is empty.')
        # Iterate over the list.
        for e in self.environments:
            self.environment_check(e)


        self.assertTrue(self.environments.svms > 0)
        self.assertTrue(self.environments.vm_count > 0)
        self.assertTrue(self.environments.svms > self.environments.vm_count)

    def environment_check(self, env):
        self.assertTrue(env.id > 0, 'No environment ID found')
        self.assertTrue(len(env.details()) > 0, env.name + ': No details found.')
        self.assertTrue(len(str(env)) > 0, env.name + ': No string conversion found.')
