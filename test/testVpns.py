import json
import os
import sys
import unittest

sys.path.append('..')
from skytap.Vpns import Vpns  # nopep8


class TestVpns(unittest.TestCase):

    def setUp(self):
        self.vpns = Vpns()

    def test_basic_vpn_check(self):
        self.assertTrue(len(self.vpns) > 0,
                        'Vpn list is empty.')

        for v in self.vpns:
            self.vpn_check(v)

    def vpn_check(self, vpn):
        self.assertTrue(vpn.id > 0, 'No vpn ID found')
        self.assertTrue(len(vpn.details()) > 0,
                        vpn.name + ': No details found.')
        self.assertTrue(len(str(vpn)) > 0,
                        vpn.name + ': No string conversion found.')
