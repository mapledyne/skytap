#!/usr/bin/env python
#
#

# import necessary modules

import sys
import traceback
import getopt
import json
import time

try:
  import requests
except ImportError:
  sys.stderr.write("You do not have the 'requests' module installed.  Please see http://docs.python-requests.org/en/latest/ for more information.")
  exit(1)

try:
  import yaml
except ImportError:
  sys.stderr.write("You do not have the 'yaml' module installed.  Please see http://pyyaml.org/wiki/PyYAMLDocumentation for more information.")
  exit(1)


# get configuration from yaml and populate variables

f = open ('config.yml')
config_data = yaml.safe_load(f)
f.close()

base_url = config_data["base_url"]
user = config_data["user"]
token = config_data["token"]
working_dir = config_data["working_dir"]
control_dir = config_data["control_dir"]
temp_dir = config_data["temp_dir"]



############################################################################ 
#### begin api interactions


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
 
#     if len(argv) > 3:
#         data = load_file(argv[3])
#     else:
#         data = None

    response =  requests.put(url, headers=requisite_headers, auth=auth, params=data)

    return response.status_code, response.text
    

def _api_post(argv):
    url, name, passwd = argv[0], argv[1], argv[2]
    
    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd) 
 
    if len(argv) > 3:
        data = load_file(argv[3])
    else:
        data = None
    
    response =  requests.post(url, headers=requisite_headers, auth=auth, data=data)
    
    return response.status_code, response.text


def _api_del(argv):
    url, name, passwd = argv[0], argv[1], argv[2]
    
    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd) 
    
    response =  requests.delete(url, headers=requisite_headers, auth=auth)
    
    return response.status_code, response.text


def rest_usage():
    print "usage: rest [put|get|post|delete] url name passwd"
    sys.exit(-1)

cmds = {
    "GET": _api_get, 
    "PUT": _api_put, 
    "POST": _api_post,
    "DELETE": _api_del
    }

def load_file(fname):
  with open(fname) as f:
    return f.read()

def rest(req, url, user, token, data=None):

#     if len(argv) < 4:
#         rest_usage()
        
    if 'HTTPS' not in url.upper():
        print "Secure connection required: HTTP not valid, please use HTTPS or https"
        rest_usage()       
        
    cmd = req.upper()
    if cmd not in cmds.keys():
        rest_usage()

    status,body=cmds[cmd](url, data)
    print
    if int(status) == 200:
        json_output = json.loads(body)
        print json.dumps(json_output, indent = 4)        
        return body
    else:
        print "Oops!  Error: status: %s\n%s" % (status, body)
        print
        
############################################################################ 
#### begin custom functions


def get_configurations():
  body = rest('get', base_url+'/configurations', user, token)
  json_output = json.loads(body)
  
  l = []
  for j in json_output:
    l.append(j.get('id'))
    
  return l
      

def get_exclusions():
  exclusions = []
  f = open(control_dir+'/exclusions-final.conf', 'r')
  for line in f:
    exclusions.append(line.split("#",1)[0].rstrip())
    
  exclusions = filter(None, exclusions)  
  
  #encode exclusions in unicode
  unicode_exclusions = [unicode(i) for i in exclusions]
  
  return unicode_exclusions
  

def suspend_configurations():
  configurations = set(get_configurations())
  exclusions = set(get_exclusions())
  suspends = list(configurations - exclusions)
  
  data = {'runstate' : 'suspended'}

  for i in suspends:
    print i
    rest('put', base_url+'/configurations/2156312?runstate=suspended', user, token, data=data)

def update_dashing(id, usage, limit):
# curl -d '{ "auth_token": "YOUR_AUTH_TOKEN", "value": 83 }' \http://localhost:3030/widgets/svm-current-usage

  dashing_url = "http://localhost:3030/widgets/"+id
  data = { "auth_token": "YOUR_AUTH_TOKEN", "value": usage, "max": limit, "current": usage,}
  requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
  }
  response = requests.post(dashing_url, data=json.dumps(data), headers=requisite_headers)
  print data
  return response.status_code, response.text
  
  
def get_quotas():
  body = rest('get', base_url+'/company/quotas/', user, token)
  json_output = json.loads(body)
  
  for j in json_output:
    id, usage, limit = j['id'], j['usage'], j['limit']
    
    if id == "concurrent_storage_size":
      usage = round( usage / 1048576.0, 1)
      limit = round( limit / 1048576.0, 1)
      print id, usage, limit
    update_dashing(id, usage, limit)
    

############################################################################ 
#### begin interface items


def usage(exitcode):

  usage="""
  
  
##########################    Welcome to Skynet    #########################

  skynet [--help] [--action=<action-name>]

OPTIONS:
  --help, -h
    prints this document
    
  --action=<action-name>, -a <action-name>
    Take an action

ACTIONS:
  'suspend' will suspend configurations that are not on the exclusions list.
  
EXAMPLES:
  skynet -a suspend 

############################################################################ 


  
"""

  try:
    exitcode
  except NameError:
    print usage
    sys.exit(-1)
  else:
    print usage
    sys.exit(exitcode)

 
# argument parser
def ui(argv):
  
# define variables to be used by getopts and sent them to null
  action = ''
  scope = ''
  
#  print 'ARGV     :', sys.argv[1:]
  
  try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'a:hs:t', ['help',
                                                          'action=',
                                                          'scope=',
                                                          ])
                                            
  except getopt.GetoptError:
    usage()
    sys.exit(2)


  for opt, arg in options:
    if opt in ('-h', '--help'):
      usage(2)
      sys.exit()

    elif opt in ( '-a', '--action' ):
      action = arg
      if action == 'suspend':
        suspend_configurations()
      elif action == 'quotas':
         while True: 
           get_quotas()
           time.sleep(15)
      elif action != 'suspend':
        usage(2)
      
    elif opt in ( '-s', '--scope' ):
      scope = arg
      usage(3)

    elif opt in ( '-t' ):
      print 'TEST ENVIRONMENT'
    
 
# call main
if __name__=='__main__':

  ui(sys.argv[1:]) 
