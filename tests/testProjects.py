import json
import os
import sys

sys.path.append('..')
from skytap.Projects import Projects  # noqa


class TestProjects(object):

    def setUp(self):
        self.projects = Projects()

    def test_basic_project_check(self):
        assert len(self.projects) > 0, 'Project list is empty.'

        for p in self.projects:
            self.project_check(p)

    def project_check(self, prj):
        assert prj.id > 0, 'no project ID found.'
        assert len(prj.name) > 0, str(prj.id) + ': no name found.'
        assert prj.user_count > 0, prj.name + ': no users found.'
        assert len(prj.details()), prj.name + ': no details found.'
