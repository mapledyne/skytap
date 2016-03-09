"""Test Skytap published services API access."""
import json
import os
import time
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa
from skytap.framework.ApiClient import ApiClient  # noqa

environments = Environments()


def test_ps_values():
    """Ensure published service capabilities are functioning."""
    e = environments.first()

    for v in e.vms:
        for i in v.interfaces:
            for s in i.services:
                assert s.id
                assert s.internal_port
                assert s.external_ip
                assert s.external_port
