"""Test Skytap interfaces API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa

environments = Environments()


def test_interface_values():
    """Ensure interface capabilities are functioning."""
    e = environments.first()
    for v in e.vms:
        for i in v.interfaces:
            assert i.id
