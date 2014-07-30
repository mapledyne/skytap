#!/usr/bin/env python

""" 
Copyright 2014 Skytap Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#------------------------------------------------------------------------

Sample code for learning and exercising the REST API.  

Note: requires the requests python module which is 
open source (Apache2 licensed) and can be installed via Pip

This code was tested with python 2.7.5
"""

import json
import requests
import sys
import traceback

    
def _api_get(argv):
    url, name, passwd = argv[0], argv[1], argv[2]
    
    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd) 
    
    response =  requests.get(url, headers=requisite_headers, auth=auth)
    
    return response.status_code, response.text


def _api_put(argv):
    url, name, passwd = argv[0], argv[1], argv[2]
    
    requisite_headers = { 'Accept' : 'application/json',
                          'Content-Type' : 'application/json'
    }
    auth = (name, passwd) 
 
    if len(argv) > 3:
        data = load_file(argv[3])
    else:
        data = None
    
    response =  requests.put(url, headers=requisite_headers, auth=auth, data=data)
    
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


def usage():
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

def rest(argv):

    if len(argv) < 4:
        usage()
        
    if 'HTTPS' not in argv[1].upper():
        print "Secure connection required: HTTP not valid, please use HTTPS or https"
        usage()       
        
    cmd = argv[0].upper()
    if cmd not in cmds.keys():
        usage()

    status,body=cmds[cmd](argv[1:])
    print
    if int(status) == 200:
        json_output = json.loads(body)
        print json.dumps(json_output, indent = 4)        
    else:
        print "Oops!  Error: status: %s\n%s" % (status, body)
        print


## run rest interactively
#rest(sys.argv[1:])        

