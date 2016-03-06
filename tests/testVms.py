"""Test Skytap Environments API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa

environments = Environments()

vms_to_check = 10


def test_vm_id():
    """Ensure VM has an ID."""
    vm_count = 0
    for e in environments:
        for v in e.vms:
            vm_count += 1
            if vm_count > vms_to_check:
                return
            assert v.id > 0, 'Env ' + str(e.id) + ': No VM id found.'


def test_vm_str_conversion():
    """Test string conversion."""
    vm_count = 0
    for e in environments:
        for v in e.vms:
            vm_count += 1
            if vm_count > vms_to_check:
                return
            assert len(str(v)) > 0


def test_vm_url_exists():
    """Test VM URL exist."""
    vm_count = 0
    for e in environments:
        for v in e.vms:
            vm_count += 1
            if vm_count > vms_to_check:
                return
            assert len(str(v.url)) > 0
