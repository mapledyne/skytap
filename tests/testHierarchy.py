"""Test multiple models, from environments downward."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa

envs = Environments()

def get_urls():
    for e in envs:
        print e.url
        for v in e.vms:
            print v.url
            for i in v.interfaces:
                print i.url
                for s in i.services:
                    print s.url
                    print s.id
                    print s.external_port
                    print s.external_ip
                    print s.internal_port



if __name__ == "__main__":
    get_urls()
