import json


class User(object):
    def __init__(self, user_json):
        self.user_data = {}
        for k, v in user_json.iteritems():
            self.user_data[k] = v
        self.user_data['name'] = self.first_name + ' ' + self.last_name

    def __getattr__(self, key):
        """Make the user values accessible.

        This allows all user values to be available via calls like:
        user.id
        """
        if key not in self.user_data:
            raise AttributeError
        return self.user_data[key]

    def details(self):
        det = ''
        for x in self.user_data:
            det += str(x) + ": " + str(self.user_data[x]) + '\n'
        return det

    def __str__(self):
        return '[' + self.id + '] ' + self.name

    def __int__(self):
        return int(self.id)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __hash__(self):
        return hash(user_data)

    def __eq__(self, other):
        return hash(self) == hash(other)
