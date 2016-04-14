from skytap.models.SkytapResource import SkytapResource


class Label(SkytapResource):

    """One Skytap label."""

    def __init__(self, label_json):
        """Init is mainly handled by the parent class."""
        super(Label, self).__init__(label_json)
