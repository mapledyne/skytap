"""Skytap API object wrapping Skytap VPNs.

This roughly translates to the Skytap API call of /v2/vpns REST call,
but gives us better access to the bits and pieces of the VPN.

If accessed via the command line (``python -m skytap.Vpns``) this will
return the quotas from Skytap in a JSON format.
"""
import sys

from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vpn import Vpn


class Vpns(SkytapGroup):

    """Set of Skytap VPNs.

    Example:
        v = skytap.Users()
        print len(v)
    """

    def __init__(self):
        """Build the VPN list from the Skytap API."""
        super(Vpns, self).__init__()
        self.load_list_from_api('/v2/vpns', Vpn)

if __name__ == '__main__':
    print(Vpns().main(sys.argv[1:]))
