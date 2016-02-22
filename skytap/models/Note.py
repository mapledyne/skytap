import datetime
import json
import skytap.framework.Utils as Utils
from skytap.models.SkytapResource import SkytapResource


class Note(SkytapResource):

    def __init__(self, note_json):
        super(Note, self).__init__(note_json)

    def __str__(self):
        return '[' + self.id + '] ' + self.text
