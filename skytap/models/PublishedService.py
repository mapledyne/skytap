"""Support for a published service resource in Skytap."""
from skytap.framework.ApiClient import ApiClient  # noqa
import skytap.framework.Utils as Utils  # noqa
from skytap.models.SkytapResource import SkytapResource  # noqa


class PublishedService(SkytapResource):

    def delete(self):
        """Delete a service. Cannot be undone!"""
        Utils.info('Deleting published service: ' + str(self.id))
        api = ApiClient()
        response = api.rest(self.url, {}, 'DELETE')
        return response
