"""Support for Skytap quotas."""
from datetime import timedelta
import json
from skytap.models.SkytapResource import SkytapResource


class Quota(SkytapResource):

    """One piece of quota information."""

    def __init__(self, quota_json):
        """Build the quota object.

        Args:
            quota_json (list): The quota data.
        """
        super(Quota, self).__init__(quota_json)

    def _calculate_custom_data(self):
        """Create a percentage used and time object, if applicable."""
        if self.limit is not None:
            self.data['pct'] = self.usage / self.limit
        if self.units == 'hours':
            self.time = timedelta(hours=self.usage)
        self.data['name'] = self.id

    def __str__(self):
        quota = self.id + " = " + str(self.usage)
        if self.units != 'integer':
            quota += "" + self.units
        return quota
