"""Support for Skytap VPNs."""
from skytap.models.SkytapResource import SkytapResource


class Vpn(SkytapResource):
    """One Skytap VPN object."""

    def __init__(self, vpn_json):
        """Create one VPN object."""
        super(Vpn, self).__init__(vpn_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Create an 'active' flag based on the status of the VPN.
        """
        self.active = self.status == 'active'
