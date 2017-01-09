"""Support for Skytap VM Exports."""
import json

from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource


class Export(SkytapResource):
    """One Skytap VM Export object."""

    def __init__(self, export_json):
        """Create one Export object."""
        super(Export, self).__init__(export_json)
        self.url = '/v2/exports/' + str(self.id)

    def delete(self):
        """Delete this export job."""
        Utils.info('Deleting job ' + str(self.id) + ' from queue.')
        api = ApiClient()
        response = api.rest(self.url,
                 {},
                 'DELETE')
        return response
