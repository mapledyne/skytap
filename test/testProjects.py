import json
import os
import sys
import unittest
import random

sys.path.append('..')
from skytap.Projects import Projects


class TestProjects(unittest.TestCase):

    def setUp(self):
        self.projects = Projects()

    def test_basic_project_check(self):
        self.assertTrue(len(self.projects) > 0,
                        'Project list is empty.')
        # Iterate over the list.
        for p in self.projects:
            a_project = str(self.projects[p])  # test string conversion

        # Get a random projet to get this and do ... something with it to check.
        one_prj = self.projects[random.choice(list(self.projects.keys()))]
        print one_prj.details()
