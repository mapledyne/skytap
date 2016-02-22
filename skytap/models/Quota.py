import json
from datetime import timedelta
from skytap.models.SkytapResource import SkytapResource


class Quota(SkytapResource):
    def __init__(self, quota_json):
        super(Quota, self).__init__(quota_json)

    def _calculate_custom_data(self):
        if self.limit is not None:
            self.data['pct'] = self.usage / self.limit
        if self.units == 'hours':
            self.time = timedelta(hours=self.usage)
        self.data['name'] = self.id

    def __str__(self):
        return "[" + self.id + "] " + str(self.usage) + " " + self.units
