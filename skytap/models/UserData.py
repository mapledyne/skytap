import json
from skytap.models.SkytapResource import SkytapResource


class UserData(SkytapResource):
    def __init__(self, contents):
        super(UserData, self).__init__(contents)

    def __str__(self):
        return self.contents

    def _clean_value(self, key, value):
        default_time = 3
        default_delay_min = 0
        default_delay_max = 31

        # Check value for shutdown_time and decide what to do with it
        if key == "shutdown_time":
            try:
                if value == "-":
                    # Permanent exclusion case
                    pass
                elif (int(value) < 0 or int(value) > 23):
                    # Should be valid time
                    value = str(default_time)
            except ValueError:
                # Not an int, revert to default
                value = str(default_time)

        # Check value for shutdown_delay and decide what to do with it
        if key == "shutdown_delay":
            try:
                if int(value) < default_delay_min:
                    # Delay smaller than minimum, set to 0
                    value = str(default_delay_min)
                elif int(value) > default_delay_max:
                    # Delay larger than maximum, set to 31
                    value = str(default_delay_max)
            except ValueError:
                # Delay is not a number, change to 0
                value = str(default_delay_min)

        # If this is valid, leave it alone. Otherwise, change the value to "-",
        # which triggers the variable itself to be removed.
        if key == "delete_environment":
            try:
                int(value)
            except ValueError:
                value = "error"

        return value

    def _get_values(self, contents):
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
                    self.data[tokens[0][:-1]] = values[tokens[0][:-1]]

        return values

    def _calculate_custom_data(self):
        if self.contents:
            values = self._get_values(self.contents)
        else:
            self.data["contents"] = ""
