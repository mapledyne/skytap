"""Functions needed to access the skynet api."""
import sys

try:
    import requests
except ImportError:
    sys.stderr.write("You do not have the 'requests' module installed.  Please see http://docs.python-requests.org/en/latest/ for more information.")
    exit(1)


requests.packages.urllib3.disable_warnings()

token = ""
user = ""
base_url = ""

def load_file(fname):
    """Load the file."""
    with open(fname) as the_file:
        return the_file.read()

def rest(url, req = 'get'):
    """Main function to be called from this module.

    send a request using method 'req' and to the url. the _rest() function
    will add the base_url to this, so 'url' should be something like '/ips'.
    """
    return _rest(req,base_url+url, user, token)

def _rest(req, url, user, token, data=None):
    """Send a rest rest request to the server."""
#     if len(argv) < 4:
#         rest_usage()

    if 'HTTPS' not in url.upper():
        print "Secure connection required: HTTP not valid, please use HTTPS or https"
        return ""

    cmd = req.upper()
    if cmd not in cmds.keys():
        return ""

    status,body=cmds[cmd](url, data)
    if int(status) == 200:
#        json_output = json.loads(body)
#        print json.dumps(json_output, indent = 4)
        return body
    else:
        print "Oops!  Error: status: %s\n%s\n" % (status, body)


def _api_get(url, data=None):
    url, name, passwd = url, user, token

    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd)

    response =  requests.get(url, headers=requisite_headers, auth=auth)

    return response.status_code, response.text


def _api_put(url, data):
    url, name, passwd = url, user, token

    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd)

    response =  requests.put(url, headers=requisite_headers, auth=auth, params=data)

    return response.status_code, response.text


def _api_post(url, data = None):
    url, name, passwd = url, user, token

    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd)

    response =  requests.post(url, headers=requisite_headers, auth=auth, data=data)

    return response.status_code, response.text


def _api_del(url, _ = None):
    url, name, passwd = url, user, token

    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd)

    response =  requests.delete(url, headers=requisite_headers, auth=auth)

    return response.status_code, response.text

cmds = {
    "GET": _api_get,
    "PUT": _api_put,
    "POST": _api_post,
    "DELETE": _api_del
    }
