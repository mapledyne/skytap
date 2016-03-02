import json
import logging
from skytap.framework.ApiClient import ApiClient
from skytap.models.SkytapResource import SkytapResource


class UserData(SkytapResource):
    def __init__(self, contents, env_url):
        super(UserData, self).__init__(contents)
        self.url = env_url + '/user_data.json'

    def __str__(self):
        return self.contents

    def add(self, key, value):
        """Add value to environment's userdata.

        Args:
            key (str): The name of the value's key.
            value (str): The value to add.

        Returns:
            str: The response from Skytap, or "{}".
        """

        add_key = True

        lines = self.contents.split("\n")

        for i in lines:
            if i != "":
                j = i.split()
                if len(j) > 0 and j[0] == (key + ":"):
                    add_key = False

        if add_key:
            logging.info('Adding key \"' + key + '\" with value \"'
                         '' + value + '\"')
            api = ApiClient()
            new_content = "" + key + ": " + value + "\n" + self.contents
            data = {"contents": new_content}
            response = api.rest(self.url, data, 'POST')
            self.data[key] = value
            self.refresh()
            return response
        else:
            logging.info('Key \"' + key + '\" with value \"' + value + '\"'
                         'already exists.')
            return "{}"

    def delete(self, key):
        """Delete key/value from environment's userdata.

        Args:
            key (str): The name of key to delete, along with value

        Returns:
            str: The response from Skytap, or "{}".
        """

        new_content = ""

        del_key = False

        lines = self.contents.split("\n")

        for i in lines:
            if i != "":
                j = i.split()
                if len(j) > 0 and j[0] == (key + ":"):
                    del_key = True
                else:
                    new_content += (i.strip() + "\n")

        if del_key:
            logging.info('Deleting key \"' + key + '\".')
            api = ApiClient()
            data = {"contents": "" + new_content}
            response = api.rest(self.url, data, 'POST')
            self.refresh()
            return response
        else:
            logging.info('Key \"' + key + '\" already exists.')
            return "{}"

    def add_line(self, text, line=-1):
        """Add line to environment's userdata.

        Args:
            text (str): line of text to be added. (Required)
            line (int): line number to add to. If too large, default to last.

        Returns:
            str: The response from Skytap.
        """

        try:
            line = int(line)
        except ValueError:
            return "{}"  # Not an integer

        lines = self.contents.split("\n")

        new_content = ""

        line_found = False
        count = 0
        for i in lines:
            if i != "":
                if line == count:
                    new_content += (text.strip() + "\n")

                    new_content += (i.strip() + "\n")

                    line_found = True
                else:
                    new_content += (i.strip() + "\n")

            count += 1

        if not line_found:
            new_content += (text.strip() + "\n")

        logging.info('Adding line: \"' + text + '\"')
        api = ApiClient()
        data = {"contents": new_content}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def delete_line(self, line):
        """Delete line from environment's userdata.

        Args:
            line (int): line number to delete.

        Returns:
            str: The response from Skytap.
        """

        line = str(line)

        lines = self.contents.split("\n")

        new_content = ""

        line_found = False
        for i in lines:
            if i != "":
                if i.strip() != line.strip():
                        new_content += (i.strip() + "\n")
                        line_found = True

        logging.info('Removing line: \"' + str(line) + '\"')
        api = ApiClient()
        data = {"contents": new_content.lstrip()}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def get_line(self, line):
        """Return content of line from environment's userdata.

        Args:
            line (int): line number to get.

        Returns:
            str: The content of the line, or "".
        """

        try:
            line = int(line)
        except ValueError:
            return ""  # Not an integer

        lines = self.contents.split("\n")

        line_found = False
        count = 0
        for i in lines:
            if line == count:
                    return i

        if not line_found:
            return ""

    def _get_values(self, contents):
        """Check userdata and set variables based on keys/values within."""
        lines = contents.split("\n")

        values = {}

        for i in lines:
            tokens = i.split()

            if len(tokens) < 2:
                continue

            # Check for valid YAML formatting in first and second tokens in each
            # line, then add those values to dict.
            if (tokens[0].endswith(":") and "#" not in tokens[0] and
                    len(tokens) > 1 and "#" not in tokens[1]):
                    # If variable is a number, make it integer
                    try:
                        values[tokens[0][:-1]] = int(tokens[1])
                    except ValueError:
                        values[tokens[0][:-1]] = tokens[1]

                    self.data[tokens[0][:-1]] = values[tokens[0][:-1]]

        return values

    def _calculate_custom_data(self):
        if self.contents:
            values = self._get_values(self.contents)
        else:
            self.data["contents"] = ""
