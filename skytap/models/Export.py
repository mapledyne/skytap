"""Support for Skytap VM Exports."""
from skytap.models.SkytapResource import SkytapResource


class Export(SkytapResource):
    """One Skytap VM Export object."""

    def __init__(self, export_json):
        """Create one Export object."""
        super(Export, self).__init__(export_json)
