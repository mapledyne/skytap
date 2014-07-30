#!/usr/bin/env python
#
#

# import necessary modules
import sys
import requests
import json

# import skynet modules
from skynet_modules.config import *
import skynet_modules.rest as rest

def get_api(path):
  data = rest.rest(('get',base_url+path,user,token))
  
# call main
if __name__=='__main__':
  get_api('configurations/')
