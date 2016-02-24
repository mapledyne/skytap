import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Projects import Projects  # nopep8


class TestProjects(unittest.TestCase):

    def setUp(self):
        self.projects = Projects()

    def test_basic_project_check(self):
        self.assertTrue(len(self.projects) > 0,
                        'Project list is empty.')

        for p in self.projects:
            self.project_check(p)

    def project_check(self, prj):
        self.assertTrue(prj.id > 0, 'no project ID found.')
        self.assertTrue(len(prj.name) > 0, str(prj.id) + ': no name found.')
        self.assertTrue(prj.user_count > 0, prj.name + ': no users found.')
        self.assertTrue(len(prj.details()), prj.name + ': no details found.')
