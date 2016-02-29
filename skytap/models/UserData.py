import json
from skytap.models.SkytapResource import SkytapResource


class UserData(SkytapResource):
    def __init__(self, contents):
        super(UserData, self).__init__(contents)

    def __str__(self):
        return self.contents

    def _clean_value(self, key, value):
        """Adjust values based on current form and return new form.

        Example case:

        if key == "number_of_mario_brothers":
            if value != "2":
                value == "2"

        By default, this function will simply return the value as is.
        """

        return value

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
                    values[tokens[0][:-1]] = self._clean_value(tokens[0][:-1],
                                                               tokens[1])
                    # If variable is a number, make it integer
                    try:
                        values[tokens[0][:-1]] = int(values[tokens[0][:-1]])
                    except ValueError:
                        pass

                    self.data[tokens[0][:-1]] = values[tokens[0][:-1]]

        return values

    def _calculate_custom_data(self):
        if self.contents:
            values = self._get_values(self.contents)
        else:
            self.data["contents"] = ""
