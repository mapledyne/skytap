"""Support for a single note in a Skytap environment or vm."""

import datetime
import json
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource


class Note(SkytapResource):

    """One note."""

    def __init__(self, note_json):
        """Build the note from the incoming JSON."""
        super(Note, self).__init__(note_json)

    def __str__(self):
        """Return just the note.

        :returns: str -- the note contents.

        """
        return self.text
