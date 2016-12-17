"""Support for Skytap IPs."""
from skytap.models.SkytapResource import SkytapResource


class IP(SkytapResource):
    """One Skytap VPN object."""

    def __init__(self, ip_json):
        """Create one VPN object."""
        super(IP, self).__init__(ip_json)
