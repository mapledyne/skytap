"""Test Skytap Environments API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # nopep8

environments = Environments()
things_to_check = 25


def test_str_vs_contents():
    """Ensure str() returns the contents."""
    count = 0
    for e in environments:
        count += 1
        assert str(e.user_data) == str(e.user_data.contents)
        for v in e.vms:
            if count > things_to_check:
                return
            count += 1
            assert str(v.user_data) == str(v.user_data.contents)
