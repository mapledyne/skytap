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

    def delete_export_job(self, export_job):
        if type (job) is not int:
            raise TypeError('Export job must be an int.')

    Utils.info('Deleting job ' +str(export_job) +
                ' from queue.')
    api = ApiClient()
    api.rest(self.url + '/v2/exports/' + str(export_job),
            {},
            'DELETE')
