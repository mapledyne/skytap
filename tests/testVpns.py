import json
import os
import sys

sys.path.append('..')
from skytap.Vpns import Vpns  # nopep8


class TestVpns(object):

    def setUp(self):
        self.vpns = Vpns()

    def test_basic_vpn_check(self):
        assert len(self.vpns) > 0, 'Vpn list is empty.'

        for v in self.vpns:
            self.vpn_check(v)

    def vpn_check(self, vpn):
        assert len(vpn.id) > 0, 'No vpn ID found'
        assert len(vpn.details()) > 0, vpn.name + ': No details found.'
        assert len(str(vpn)) > 0, vpn.name + ': No string conversion found.'
