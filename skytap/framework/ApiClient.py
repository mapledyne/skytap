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
            'GET': requests.get,
            'PUT': requests.put,
            'POST': requests.post,
            'DELETE': requests.delete
        }

        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def _check_response(self, resp, attempts=1):
        if resp is None:
            raise ValueError('A response wasn\'t received')

        if 200 <= resp.status_code < 300:
            return True

        # If we made it this far, we need to handle an exception
        if attempts >= self.max_attempts or (resp.status_code != 429 and
                                             resp.status_code != 423):
            raise Exception(json.loads(resp.text))

        if resp.status_code == 423:  # "Busy"
            if 'Retry-After' in resp.headers:
                time.sleep(int(resp.headers['Retry-After']) + 1)
            else:
                time.sleep(10)  # Skytap's recommendation for a default
            return False

        # Assume we're going to retry with exponential backoff
        # Should only get here on a 429 "too many requests" but it's
        # not clear from Skytap what their limits are on when we should retry.
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

    def rest(self, url, params={}, req='get', data=None):
        """Call the REST API, returning all results.

        This calls the actual REST API, then checks the returning headers in
        case there is a range returned, implying that the full range wasn't
        returned originally. If there's a range, then make a second call asking
        for everything.

        This defeats the pagination that Skytap uses in their v2 API, but is
        useful for us given how we use the API.
        """
        if not url.upper().startswith('HTTP'):
            url = self.base_url + url

        first_call = self._rest(req, url, params, data)
        if self.last_range == 0:
            return first_call

        params['offset'] = 0
        params['count'] = self.last_range

        return self._rest(req, url, params, data)

    def _rest(self, req, url, params={}, data=None, attempts=0):
        """Send a rest rest request to the server."""

        if 'HTTPS' not in url.upper():
            return "Secure connection required: Please use HTTPS or https"

        cmd = req.upper()
        if cmd not in self.cmds.keys():
            raise ValueError("Command type (" + cmd + ") not recognized.")

        url += self._dict_to_query_params(params)

        response = self.cmds[cmd](url,
                                  headers=self.headers,
                                  auth=self.auth,
                                  params=data)

        self.last_status = response.status_code
        self.last_headers = response.headers
        self.last_range = 0
        if "content-range" in self.last_headers:
            self.last_range = self.last_headers["content-range"].split("/")[1]

        attempts += 1
        if self._check_response(response, attempts):
            return json.dumps(json.loads(response.text), indent=4)
        else:
            return self._rest(req, url, params, data, attempts)
