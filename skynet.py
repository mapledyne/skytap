#!/usr/bin/env python
#
#

# set some variables

base_url = 'https://cloud.skytap.com'
user = 'skynet@fulcrum.net'
token = '55b5e1a75ce9a122db3c976d161f96b15b5eb825'

working_dir = '/Users/thewellington/Development/skynet'              # this is the path to the skynet.py file
control_dir = '/Users/thewellington/Development/skytap-control'      # this is the path to the skytap-control directory
temp_dir = '/tmp'


# import necessary modules
import sys
import requests
import json
import getopt

# import skynet modules
from skynet_modules.config import *
import skynet_modules.rest as rest

def get_api(path):
  data = rest.rest(('get',base_url+path,user,token))
############################################################################ 
 
# argument parser
def ui(argv):
  
# define variables to be used by getopts and sent them to null
  action = ''
  scope = ''
  
  usage = """
##########    Welcome to Skynet    ##########

At this time Skynet takes two arguments at most.  Here are your options
  
  -h --help     Produces this help file
  -a --action   Indicates the action you wish to take
  -s --scope    Defines the scope of the action(s)
  
EXAMPLES:

skynet -a suspend -s limited
  
"""
  print 'ARGV     :', sys.argv[1:]
  
  try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'a:hs:', ['help',
                                                          'action=',
                                                          'scope=',
                                                          ])
                                            
  except getopt.GetoptError:
    print usage
    sys.exit(2)


  print 'OPTIONS    :', options

  for opt, arg in options:
    if opt in ('-h', '--help'):
      print usage
      sys.exit()

    elif opt in ( '-a', '--action' ):
      action = arg
    
    elif opt in ( '-s', '--scope' ):
      scope = arg
    
  print 'ACTION   :', action
  print 'SCOPE      :', scope
  print 'REMAINING  :', remainder




 
# call main
if __name__=='__main__':

  ui(sys.argv[1:]) 
