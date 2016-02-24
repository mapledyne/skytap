"""Skytap API object wrapping Skytap VPNs.

This roughly translates to the Skytap API call of /v2/vpns REST call,
but gives us better access to the bits and pieces of the VPN.
"""
import json
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Vpn import Vpn


class Vpns(SkytapGroup):

    """Set of Skytap VPNs.

    :Example:
    >>> v = Users()
    >>> print len(v)
    8
    """

    def __init__(self):
        """Build the VPN list from the Skytap API."""
        super(Vpns, self).__init__()
        self.load_list_from_api('/v2/vpns', Vpn)

if __name__ == '__main__':
    vpns = Vpns()
    print(json.dumps(vpns.json, indent=4))
