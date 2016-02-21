from collections import Iterator
from skytap.framework.ApiClient import ApiClient
import json


class SkytapGroup(ApiClient):
    def __init__(self):
        super(SkytapGroup, self).__init__()
        self.data = {}
        self.itercount = 0

    def load_list_from_api(self, url, target):
        self.load_list_from_json(self.rest(url), target)

    def load_list_from_json(self, json_list, target):
        self.data = {}
        if isinstance(json_list, str):
            self.json = json.loads(json_list)
        elif isinstance(json_list, list):
            self.json = json_list
        else:
            raise TypeError
        for j in self.json:
            self.data[int(j['id'])] = target(j)

    def __len__(self):
        return len(self.data)

    def __str__(self):
        data_str = ''
        for u in self.data:
            data_str += str(self.data[u]) + '\n'
        return data_str

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return self

    def next(self):
        if self.itercount >= len(self.data):
            raise StopIteration
        n = self.data.keys()[self.itercount]
        self.itercount += 1
        return self.data[n]

    def keys(self):
        return self.data.keys()

    def __contains__(self, key):
        return self.data.contains(key)
