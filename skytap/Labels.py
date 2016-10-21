"""Support for Skytap API access to the labels."""
from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.Label import Label
from skytap.models.SkytapGroup import SkytapGroup


class Labels(SkytapGroup):
    """Set of Skytap labels."""

    def __init__(self, labels_json=None, url=None):
        """Build an initial list of labels."""
        super(Labels, self).__init__()
        if not labels_json:
            self.load_list_from_api('/v2/label_categories', Label,
                                    {'scope': 'company'})
        else:
            self.load_list_from_json(labels_json, Label,
                                     url + '/labels',
                                     {'scope': 'company'})

    def create(self, name, single_value):
        """Create label that is single or multi-valued."""
        if not self.url.endswith("label_categories"):
            return "Cannot create label. Did you mean to use \"add()\"?"

        Utils.info("Creating Label: " + name + ""
                   ". Single-value: " + str(single_value))
        api = ApiClient()
        data = [{"name": name, "single-value": single_value}]
        response = api.rest(self.url, data, "POST")
        self.refresh()
        return response

    def add(self, value, category):
        """Add label to environment or VM."""
        if self.url.endswith("label_categories"):
            return "Cannot add label. Did you mean to use \"create()\"?"

        Utils.info("Adding Label to " +
                   category +
                   " with value " +
                   value + ".")
        api = ApiClient()
        data = [{"label_category": category, "value": value}]
        response = api.rest(self.url, data, "PUT")
        self.refresh()
        return response

    def disable(self, label_id):
        """Disable a label category (the closest thing to deleting)."""
        if not self.url.endswith("label_categories"):
            return "Can only disable label categories."

        Utils.info("Disabling label category of id " + str(label_id) + ".")
        api = ApiClient()
        data = {"enabled": "False"}
        response = api.rest(self.url + "/" + str(label_id), data, "PUT")
        self.refresh()
        return response

    def enable(self, label_id):
        """Enable a label category."""
        if not self.url.endswith("label_categories"):
            return "Can only enable label categories."

        Utils.info("Enabling label category of id " + str(label_id) + ".")
        api = ApiClient()
        data = {"enabled": "True"}
        response = api.rest(self.url + "/" + str(label_id), data, "PUT")
        self.refresh()
        return response
