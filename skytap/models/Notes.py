import json
import logging
from skytap.framework.ApiClient import ApiClient
from skytap.models.Note import Note
from skytap.models.SkytapGroup import SkytapGroup


class Notes(SkytapGroup):
    def __init__(self, note_json, env_url):
        super(Notes, self).__init__()
        self.load_list_from_json(note_json, Note)
        self.url = env_url + '/notes.json'

    def add(self, note):
        logging.debug('Adding note: ' + note)
        api = ApiClient()
        data = {"text": note}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def delete(self, note):
        if note is None:
            return False
        if not isinstance(note, Note):
            raise TypeError
        logging.debug('Deleting note ID: ' + str(note.id))
        api = ApiClient()
        url = self.url.replace('.json', '/' + str(note.id))
        response = api.rest(url,
                            {},
                            'DELETE')
        self.refresh()
        return response

    def oldest(self):
        target = None
        for n in self.data:
            if target is None:
                target = self.data[n]
                continue
            if self.data[n].updated_at > target.updated_at:
                target = self.data[n]
        return target

    def newest(self):
        target = None
        for n in self.data:
            if target is None:
                target = self.data[n]
                continue
            if self.data[n].updated_at < target.updated_at:
                target = self.data[n]
        return target

    def delete_all(self):
        logging.debug('Deleting all notes.')
        keys = self.data.keys()
        count = len(keys)
        for key in keys:
            self.delete(self.data[key])
        self.refresh()
        return count

    def refresh(self):
        if len(self.url) == 0:
            return KeyError
        api = ApiClient()
        note_json = api.rest(self.url)
        self.load_list_from_json(note_json, Note)
