"""Skytap API object wrapping Skytap Public IPs.

This roughly translates to the Skytap API call of /v2/ips REST call,
but gives us better access to the bits and pieces of the VPN.

If accessed via the command line (``python -m skytap.PublicIPs``) this will
return the Public IP info from Skytap in a JSON format.
"""
import sys

from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.IP import IP


class PublicIPs(SkytapGroup):
    """Set of Skytap Public IPs.

    Example:
        ips = skytap.PublicIPs()
        print len(ips)
    """

    def __init__(self):
        """Build the IP list from the Skytap API."""
        super(PublicIPs, self).__init__()
        self.load_list_from_api('/v2/ips', IP)


if __name__ == '__main__':
    print(PublicIPs().main(sys.argv[1:]))
