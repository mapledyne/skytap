"""Support for a Public IP resource in Skytap."""
from skytap.models.SkytapResource import SkytapResource  # noqa


class PublicIP(SkytapResource):
    """One Public IP service object."""

    def __init__(self, ip_json):
        """Create one PublicIP object."""
        super(PublicIP, self).__init__(ip_json)
