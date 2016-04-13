from skytap.framework.ApiClient import ApiClient
import skytap.framework.Utils as Utils
from skytap.models.Label import Label
from skytap.models.SkytapGroup import SkytapGroup


class Labels(SkytapGroup):
    """Set of Skytap labels."""

    def __init__(self):
        """Build an initial list of labels."""
        super(Labels, self).__init__()
        self.load_list_from_api('/v2/label_categories',
                                Label,
                                {'scope': 'company'})

    def create(self, name, single_value):
        """Create label that is single or multi-valued."""
        Utils.info("Adding Label: " + name + ""
                   ". Single-value: " + str(single_value))
        api = ApiClient()
        data = {"name": name, "single-value": single_value}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response
