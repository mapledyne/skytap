#!/usr/bin/env python
"""This app encapsulates all of our interactions with the Skytap API."""
import argparse
import inspect
import json
import os
import sys
import textwrap

import skynet_api as api
import skynet_actions as actions

try:
    import yaml
except ImportError:
    sys.stderr.write("You do not have the 'yaml' module installed. " +
                     "Please see http://pyyaml.org/wiki/PyYAMLDocumentation " +
                     "for more information.")
    exit(1)

try:
    import requests
except ImportError:
    sys.stderr.write("You do not have the 'requests' module installed. " +
                     "Please see http://docs.python-requests.org/en/latest/ " +
                     "for more information.")
    exit(1)

# SSL certs can't be checked using the default libraries. This causes an SSL
# warning on every call, which floods the screen, making using this script
# interactively much harder. Disabling warnings is sad, but was the only way
# we found around it.
requests.packages.urllib3.disable_warnings()
config_data = {}
try:
    f = open(os.path.dirname(os.path.realpath(sys.argv[0])) + "/config.yml")
    config_data = yaml.safe_load(f)
    f.close()
except IOError:
    config_data["base_url"] = ""
    config_data["user"] = ""
    config_data["token"] = ""
    config_data["control_dir"] = ""
    config_data["temp_dir"] = ""

api.base_url = config_data["base_url"]
api.user = config_data["user"]
api.token = config_data["token"]

working_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
control_dir = config_data["control_dir"]
temp_dir = config_data["temp_dir"]


def rest_usage():
    """Print rest / app usage."""
    print "usage: rest [put|get|post|delete] url name passwd"
    sys.exit(-1)


def update_dashing(widget_id, usage_value, limit, status):
    """Update dashing with some piece of info."""
    # curl -d '{ "auth_token": "YOUR_AUTH_TOKEN", "value": 83 }'
    # \http://localhost:3030/widgets/svm-current-usage

    dashing_url = "http://localhost:3030/widgets/"+widget_id
    data = {"auth_token": "YOUR_AUTH_TOKEN", "value": usage_value,
            "max": limit, "current": usage, "status": status}
    requisite_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}
    response = requests.post(dashing_url, data=json.dumps(data),
                             headers=requisite_headers)
    return response.status_code, response.text


def get_quotas():
    """Return the quotas info from Skytap API."""
    body = api.rest('/company/quotas')
    json_output = json.loads(body)

    for j in json_output:
        skytap_id, skytap_usage, limit = j['id'], j['usage'], j['limit']
        status = ""

        if limit is not None:
            if usage * 100 / limit >= 90:
                status = 'warning'

                if (skytap_id == "concurrent_public_ips"
                   or skytap_id == "concurrent_netowrks"):
                    if status == "warning":
                        status = 'danger'

        if skytap_id == "concurrent_storage_size":
            skytap_usage = round(skytap_usage / 1048576.0, 1)
            limit = round(limit / 1048576.0, 1)

        if skytap_id != "concurrent_public_ips":
            update_dashing(skytap_id, skytap_usage, limit, status)


def banner_line(msg=''):
    """A banner line (functionally an <hr>) for the help page."""
    if len(msg) > 0:
        msg = '  ' + msg + '  '
    return '\n{:#^76}\n'.format(msg)


def usage_general():
    """Print the general usage statement for the app.

    This will pring the general usage, then look up possible actions,
    based on the actions module, and add those to the help as well.
    """
    usage_msg = """skynet [--help] [--action <action-name>] [--user <userid>]

OPTIONS:
    --help/-h : Prints this document
    --help/-h <action-name> : More detailed help on an action
    --action/-a <action-name> : Run specified action
    --user/-u <userid> : Provide user id to actions that require it
    --env/-e <environmentid> : Provide environment to actions that require it

EXAMPLE:
    skynet -a suspend
"""
    print (banner_line('Welcome to Skynet') + usage_msg +
           banner_line() + "ACTIONS:")
    action_list = inspect.getmembers(actions)
    for n, v in action_list:
        if n.startswith("_"):  # We want to skip all the built in stuff
            continue
        use_help = inspect.getdoc(v)
        use_help = use_help.splitlines()[0]
        use_help = "\n\t".join(textwrap.wrap(use_help, 68 - 3 - len(n)))
        print "    " + n + " : " + use_help

    print banner_line()


def usage_detailed(detail):
    """Print detailed help on one available action."""
    print banner_line('Welcome to Skynet')

    try:
        function = getattr(actions, detail)
        usage_detail = inspect.getdoc(function)
        print "Extended help for action: " + detail + "\n"
        print usage_detail
    except AttributeError:
        print "No action by this name found: " + str(detail) + "\n"
        print "Available actions are:\n"
        action_list = inspect.getmembers(actions)
        for n, v in action_list:
            if n.startswith("_"):  # We want to skip all the built in stuff
                continue
            use_help = inspect.getdoc(v)
            use_help = use_help.splitlines()[0]
            use_help = "\n\t\t".join(textwrap.wrap(use_help, 68 - 3 - len(n)))
            print "\t" + n + " : " + use_help + ""

    print banner_line()


def usage(detail=""):
    """Display the usage for the app.

    If there's a 'detail' (action) passed, display more specific
    info on that action, otherwise display general help. These two fuctions are
    split up into two functions (usage_detail and usage_general) simply for
    code clarity.
    """
    if detail == "":
        usage_general()
    else:
        usage_detailed(detail)
    sys.exit(1)

# call main
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False, argument_default='')
    parser.add_argument('-a', '--action', action='store')
    # --user and --env are simply aliases for the same thing (the parameter
    # passed to the action), but are both here for more clarity on the command
    # line.
    parser.add_argument('-u', '--user', '-e', '--env', action='store')
    parser.add_argument('-h', '--help', action='store', nargs='*')

    args = parser.parse_args()
    if args.help != '':
        usage(" ".join(args.help))

    try:
        f = getattr(actions, args.action)
        print f(args.user)

    except AttributeError:
        usage(args.action)
