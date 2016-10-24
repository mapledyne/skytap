"""Support for a single note in a Skytap environment or vm."""
from skytap.models.SkytapResource import SkytapResource


class Note(SkytapResource):
    """One note."""

    def __init__(self, note_json):
        """Create one Note."""
        super(Note, self).__init__(note_json)

    def __str__(self):
        """Represent the Note as a string."""
        return self.text
