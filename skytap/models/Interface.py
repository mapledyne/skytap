"""Support for an interface resource in Skytap."""
import json

from skytap.framework.ApiClient import ApiClient  # noqa
from skytap.models.PublishedServices import PublishedServices  # noqa
from skytap.models.SkytapResource import SkytapResource  # noqa


class Interface(SkytapResource):

    def __getattr__(self, key):
        if key == 'services':
            api = ApiClient()
            services_json = json.loads(api.rest(self.url))
            self.services = PublishedServices(services_json["services"],
                                              self.url)
            return self.services

        return super(Interface, self).__getattr__(key)
