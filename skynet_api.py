"""Functions needed to access the skynet api."""
import json
from skynet_config import config
import sys

try:
    import requests
except ImportError:
    sys.stderr.write("You do not have the 'requests' module installed. " +
                     "Please see http://docs.python-requests.org/en/latest/ " +
                     "for more information.")
    exit(1)


requests.packages.urllib3.disable_warnings()

last_headers = None
last_status = 0
last_range = 0

cmds = {
    "GET": requests.get,
    "PUT": requests.put,
    "POST": requests.post,
    "DELETE": requests.delete
}


def load_file(fname):
    """Load the file."""
    with open(fname) as the_file:
        return the_file.read()


def rest(url, req='get', data=None):
    """Call the REST API, returning all results.

    This calls the actual REST API, then checks the returning headers in
    case there is a range returned, implying that the full range wasn't
    returned originally. If there's a range, then make a second call asking for
    everything.

    This defeats the pagination that Skytap uses in their v2 API, but is useful
    for us given how we use the API.
    """
    first_call = _rest(req, config.base_url + url, data)
    if last_range == 0:
        return first_call

    new_url = url
    if "?" not in new_url:
        new_url += "?"
    else:
        new_url += "&"
    new_url += "count=" + str(last_range) + "&offset=0"

    return _rest(req, config.base_url + new_url, data)


def _rest(req, url, data=None):
    """Send a rest rest request to the server."""
    global last_status, last_headers, last_range

    requisite_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}

    auth = (config.user, config.token)
    if 'HTTPS' not in url.upper():
        return "Secure connection required: Please use HTTPS or https"

    cmd = req.upper()
    if cmd not in cmds.keys():
        return "Command type (" + cmd + ") not recognized."

#    status, body = cmds[cmd](url, data)
    response = cmds[cmd](url,
                         headers=requisite_headers,
                         auth=auth,
                         params=data)

    last_status = response.status_code
    last_headers = response.headers
    last_range = 0
    if "content-range" in last_headers:
        last_range = last_headers["content-range"].split("/")[1]

    if int(response.status_code) != 200:
        return "Oops!  Error: status: %s\n%s\n" % (last_status, response.text)

    return json.dumps(json.loads(response.text), indent=4)
