"""Support for a Public IP resource in Skytap."""
from skytap.framework.ApiClient import ApiClient  # noqa
import skytap.framework.Utils as Utils  # noqa
from skytap.models.SkytapResource import SkytapResource  # noqa


class PublicIP(SkytapResource):
    """One Public IP service object."""

    def attach(self):
        """Attach a public IP to a NIC."""


    # def detach(self):
    #     """Detach a public IP from a NIC."""
    #
    # def acquire(self):
    #     """Acquire a public IP for use in a region."""
    #
    # def release (self):
    #     """Release a public IP. Warning: Cannot be undone."""
