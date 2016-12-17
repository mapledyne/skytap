"""Support for Skytap IPs."""
from skytap.models.SkytapResource import SkytapResource


class PublicIP(SkytapResource):
    """One Skytap Public IP object."""

    def __init__(self, ip_json):
        """Create one VPN object."""
        super(PublicIP, self).__init__(ip_json)
