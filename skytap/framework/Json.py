from datetime import datetime
import json


class SkytapJsonEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)

        if (isinstance(o, datetime)):
            return o.isoformat()

        try:
            ret = json.loads(o.json())
        except AttributeError:
            raise
        else:
            return ret

        return json.JSONEncoder.default(self, o)
