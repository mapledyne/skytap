import json
import os
import sys

sys.path.append('..')
from skytap.Quotas import Quotas  # nopep8


class TestProjects(object):

    def setUp(self):
        self.quotas = Quotas()

    def test_basic_project_check(self):
        assert len(self.quotas) > 0, 'Quota list is empty.'

        for q in self.quotas:
            self.quota_check(q)

    def quota_check(self, quota):
        assert len(quota.id) > 0, 'no quota ID found.'
        assert quota.usage > 0, quota.id + ': no usage found.'
        assert len(quota.units) > 0, quota.id + ': no units found.'
        if quota.limit is not None:
            assert quota.usage <= quota.limit
            assert quota.pct == quota.usage / quota.limit
        if quota.units == 'hours':
            assert quota.time.seconds > 0
        assert len(str(quota)) > 0, quota.id + ': string conversion failed.'
