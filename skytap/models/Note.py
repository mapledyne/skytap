from skytap.models.SkytapResource import SkytapResource
import json


class Note(SkytapResource):

    def __init__(self, note_json):
        super(Note, self).__init__(note_json)

    def __str__(self):
        return '[' + self.id + '] ' + self.text
