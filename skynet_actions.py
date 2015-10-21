"""skynet_actions is the actual actions available to the skynet function.

To make a new action, add a new function to this class. The docstring is
used to make the usage info available to the end user, and the name of the
function is the name of the action as exposed to the user.
"""
import json as _json
import skynet_api as _api


def vm_detail(vm_id):
    """Get the detailed information from a VM id."""
    body = _api.rest('/vms/' + vm_id)
    jbody = _json.loads(body)
    return jbody


def exclusions():
    """Get list of exclusions from the exclusions file.

    This action doesn't query the API, but instead looks for the
    exclusions-final.conf file in the control_dir
    (specified in the config.yml).

    This file should be updated from git regularly, so here we're just reading
    the current contents to know what machines should not be suspended.

    See the exclusions file for details on its format.
    """
    exclusion_list = []
    exclusions_file = open(_api.control_dir + '/exclusions-final.conf', 'r')
    for line in exclusions_file:
        exclusion_list.append(line.split("#", 1)[0].rstrip())

    exclusion_list = [item for item in exclusions if item]
    # was: = filter(None, exclusions)

    # encode exclusions in unicode
    unicode_exclusions = [unicode(i) for i in exclusion_list]

    return unicode_exclusions


def suspend():
    """Suspend the appropriate configurations.

    This takes a set of the environments (see action env for a sample list) and
    removes any environment in the exclusion list (see action exclusions for a
    sample list) and then issues a suspend command.

    Warning: This action will actively suspend environments. If exclusions is
    not up to date, this could suspend everything in skytap.
    """
    configurations = set(env())
    exclusion_list = set(exclusions())
    suspends = list(configurations - exclusion_list)

    data = {'runstate': 'suspended'}

    for i in suspends:
        print 'Suspending environment: ' + i
        _api.rest('/configurations/' + i + '?runstate=suspended',
                  'PUT', data=data)


def env(_=None):
    """Return a simple list of environments (configurations).

    Sample output:

    [
        "437940",
        "561948",
        "1111664"
    ]
    """
    json_output = _json.loads(users())
    envs = []
    for j in json_output:
        envs = envs + user_env(j.get('id'))
    return _json.dumps(envs)


def env_full(_=None):
    """Return a detailed list of environments.

    Sample output:
    [
      {
        "url": "https://cloud.skytap.com/configurations/2836084",
        "error": "",
        "id": "2836084",
        "name": "XO Master"
      },
      {
        "url": "https://cloud.skytap.com/configurations/3168668",
        "error": "",
        "id": "3168668",
        "name": "XO Production"
      },
      {
        "url": "https://cloud.skytap.com/configurations/3942800",
        "error": "",
        "id": "3942800",
        "name": "XO CI Testing - IT"
      }
    ]
    """
    json_output = _json.loads(users())
    envs = []
    for j in json_output:
        envs = envs + user_env_full(j.get('id'))
    return _json.dumps(envs)


def user_env(user_id):
    """Get a list of environments associated with a particular user."""
    body = _api.rest('/users/'+user_id)
    env_list = []
    jbody = _json.loads(body)
    conf = jbody.get('configurations')
    for c in conf:
        env_list.append(c.get('id'))
    return env_list


def user_env_full(user_id):
    """Get detailed environment details.

    Gets details for environments associated with a particular user_id.
    """
    body = _api.rest('/users/'+user_id)
    jbody = _json.loads(body)
    conf = jbody.get('configurations')
    return conf


def users(_=None):
    """Get the basic user list.

    Sample output:
    [
      {
        "id": "14414",
        "url": "https://cloud.skytap.com/users/14414",
        "login_name": "phaury@fulcrum.net",
        "first_name": "Paul",
        "last_name": "Haury",
        "title": "",
        "email": "phaury@fulcrum.net",
        "created_at": "2012-01-02T12:43:05-08:00",
        "deleted": false
      }
    ]
    """
    body = _api.rest('/users')
    return body


def quotas(_=None):
    """Get Skytap quotas and basic info on the Skytap service.

    Sample output:
    [
      {
        "id": "concurrent_storage_size",
        "quota_type": "concurrent_storage_size",
        "units": "MB",
        "limit": 184320000,
        "usage": 103195962,
        "subscription": 122880000,
        "max_limit": 184320000
      }
    ]

    Full list of ids returned:
        concurrent_vms, concurrent_svms, cumulative_svms,
        concurrent_storage_size, concurrent_networks, concurrent_public_ips
    """
    body = _api.rest('/company/quotas')
    return body


def ips(_=None):
    """Get all public IPs assigned by Skytap.

    A return will look something like the JSON below. Unused IPs
    will have an empty 'nics' variable, and used ones will include what
    nic/vm is using a public IP in the same variable.

    [
      {
        "id": "76.191.119.24",
        "address": "76.191.119.24",
        "region": "US-West",
        "nics": [
          {
            "id": "/vms/5832366/interfaces/nic-2511996-5899928-0",
            "deployed": false
          }
        ],
        "vpn_id": null
      },
      {
        "id": "76.191.119.34",
        "address": "76.191.119.34",
        "region": "US-West",
        "nics": [],
        "vpn_id": null
      }
    ]
    """
    body = _api.rest('/ips')
    return body


def vms(environment):
    """Get a list of VMs for a given environment.

    A return will look something like the JSON below, including information
    on the environment itself, and detailed information on each VM in the
    environment.

    {
      "id": "4693564",
      "url": "https://cloud.skytap.com/configurations/4693564",
      "name": "XO PRD Hotfix",
      "error": "",
      "runstate": "running",
      "description": null,
      "suspend_on_idle": null,
      "routable": false,
      "vms": [
        {
          "id": "6142798",
          "name": "Load Balance",
          "runstate": "running",
          "hardware": {
            "cpus": 2,
            "supports_multicore": false,
            "cpus_per_socket": 1,
            "ram": 2048,
            "svms": 2,
            "guestOS": "centos-64",
            "max_cpus": 12,
            "min_ram": 256,
            "max_ram": 131072,
            "vnc_keymap": null,
            "uuid": null,
            "disks": [
              {
                "id": "disk-2661512-6214440-scsi-0-0",
                "size": 25600,
                "type": "SCSI",
                "controller": "0",
                "lun": "0"
              },
              {
                "id": "disk-2661512-6214440-scsi-0-1",
                "size": 25600,
                "type": "SCSI",
                "controller": "0",
                "lun": "1"
              }
            ],
            "storage": 51200,
            "upgradable": true,
            "instance_type": null,
            "time_sync_enabled": true,
            "copy_paste_enabled": true,
            "nested_virtualization": false
          },
          "error": false,
          "asset_id": null,
          "interfaces": [
            {
              "id": "nic-2661512-6214440-0",
              "ip": "192.168.1.1",
              "hostname": "lb",
              "mac": "00:50:56:03:ad:fc",
              "services_count": 1,
              "services": [
                {
                  "id": "8446",
                  "internal_port": 8446,
                  "external_ip": "services-uswest.skytap.com",
                  "external_port": 25594
                }
              ],
              "public_ips_count": 0,
              "public_ips": [],
              "vm_id": "6142798",
              "vm_name": "Load Balance",
              "status": "Running",
              "nat_addresses": {
                "network_nat_addresses": [
                  {
                    "network_id": 1153576,
                    "ip_address": "192.168.80.147"
                  }
                ],
                "vpn_nat_addresses": [
                  {
                    "vpn_id": "vpn-661182",
                    "ip_address": "172.16.0.153"
                  }
                ]
              },
              "network_id": "2825244",
              "network_name": "Default",
              "network_type": "automatic",
              "network_subnet": "192.168.1.0/24",
              "nic_type": "e1000"
            }
          ],
          "notes": [],
          "labels": [],
          "credentials": [
            {
              "id": "4911248",
              "text": "40583"
            }
          ],
          "desktop_resizable": true,
          "local_mouse_cursor": true,
          "maintenance_lock_engaged": false,
          "region_backend": "skytap",
          "created_at": "2015/07/15 21:53:31 -0700",
          "can_change_object_state": true,
          "configuration_url":
                        "https://cloud.skytap.com/configurations/4693564"
        }
    }
    """
    body = _api.rest('/configurations/' + environment)
    return body


def get_documentation():
    """Return relevant information to be used in auto-documentation."""
    json_output = _json.loads(users())
    envs = []
    for j in json_output:
        envs = envs + user_env_full(j.get('id'))
    envsObj = _json.dumps(envs)
    print "The start link is " + envsObj["url"]
    print "nothing here yet!"
