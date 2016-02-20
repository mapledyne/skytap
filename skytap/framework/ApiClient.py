"""Functions needed to access the skynet api."""
import json
import requests
import six
from skytap.framework.Config import Config
import sys

requests.packages.urllib3.disable_warnings()


class ApiClient(object):

    def __init__(self):
        self.base_url = Config.base_url
        self.api_user = Config.user
        self.api_token = Config.token

        if not self.base_url:
            raise ValueError('Invalid base_url')

        if not self.api_user:
            raise ValueError('Invalid api_user')

        if not self.api_token:
            raise ValueError('Invalid api_token')

        self.auth = (self.api_user, self.api_token)

        self.max_attempts = 4
        self.last_headers = None
        self.last_status = 0
        self.last_range = 0

        self.cmds = {
            "GET": requests.get,
            "PUT": requests.put,
            "POST": requests.post,
            "DELETE": requests.delete
        }

        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def _check_response(self, resp, attempts=1):
        if resp is None:
            raise ValueError("A response wasn't received")

        if 200 <= resp.status_code < 300:
            return True

        # TODO: this should also handle 423 returns ("busy") which have a retry-after timer.
        # If we made it this far, we need to handle an exception
        if attempts >= self.max_attempts or resp.status_code != 429:
            raise OktaError(json.loads(resp.text))

        # Assume we're going to retry with exponential backoff
        time.sleep(2 ** (attempts - 1))

        return False

    @staticmethod
    def _dict_to_query_params(d):
        if d is None or len(d) == 0:
            return ''

        param_list = [param + '=' +
                      (str(value).lower()
                       if type(value) == bool else str(value))
                      for param, value in six.iteritems(d)
                      if value is not None]
        return '?' + "&".join(param_list)

    def rest(self, url, req='get', data=None):
        """Call the REST API, returning all results.

        This calls the actual REST API, then checks the returning headers in
        case there is a range returned, implying that the full range wasn't
        returned originally. If there's a range, then make a second call asking
        for everything.

        This defeats the pagination that Skytap uses in their v2 API, but is
        useful for us given how we use the API.
        """
        first_call = self._rest(req, self.base_url + url, data)
        if self.last_range == 0:
            return first_call

        new_url = url
        if "?" not in new_url:
            new_url += "?"
        else:
            new_url += "&"
        new_url += "count=" + str(self.last_range) + "&offset=0"

        return self._rest(req, self.base_url + new_url, data)

    def _rest(self, req, url, data=None):
        """Send a rest rest request to the server."""

        if 'HTTPS' not in url.upper():
            return "Secure connection required: Please use HTTPS or https"

        cmd = req.upper()
        if cmd not in self.cmds.keys():
            return "Command type (" + cmd + ") not recognized."

    #    status, body = cmds[cmd](url, data)
        response = self.cmds[cmd](url,
                                  headers=self.headers,
                                  auth=self.auth,
                                  params=data)

        self.last_status = response.status_code
        self.last_headers = response.headers
        self.last_range = 0
        if "content-range" in self.last_headers:
            self.last_range = self.last_headers["content-range"].split("/")[1]

        if int(response.status_code) != 200:
            return "Oops!  Error: status: %s\n%s\n" % (last_status,
                                                       response.text)

        return json.dumps(json.loads(response.text), indent=4)
