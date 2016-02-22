import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Quotas import Quotas  # nopep8


class TestProjects(unittest.TestCase):

    def setUp(self):
        self.quotas = Quotas()

    def test_basic_project_check(self):
        self.assertTrue(len(self.quotas) > 0,
                        'Quota list is empty.')

        for q in self.quotas:
            self.quota_check(q)

    def quota_check(self, quota):
        self.assertTrue(len(quota.id) > 0, 'no quota ID found.')
        self.assertTrue(quota.usage > 0, quota.id + ': no usage found.')
        self.assertTrue(len(quota.units) > 0, quota.id + ': no units found.')
        if quota.limit is not None:
            self.assertTrue(quota.usage <= quota.limit)
        if quota.units == 'hours':
            self.assertTrue(quota.time.seconds > 0)
        self.assertTrue(len(str(quota)) > 0, quota.id + ': string conversion failed.')  # nopep8
