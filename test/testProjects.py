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
            self.project_check(p)  # test string conversion

    def project_check(self, prj):
        self.assertTrue(prj.id > 0, 'no project ID found.')
        self.assertTrue(len(prj.name) > 0, prj.id + ': no name found.')
        self.assertTrue(prj.user_count > 0, prj.name + ': no users found.')
#        self.assertTrue(prj.configuration_count > 0, prj.name + ': no environments found.')
        self.assertTrue(len(prj.details()), prj.name + ': no details found.')
