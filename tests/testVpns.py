import json
import os
import sys

sys.path.append('..')
from skytap.Vpns import Vpns  # noqa

vpns = Vpns()


def test_vpn_count():
    """Test VPN count."""
    assert len(vpns) > 0, 'Vpn list is empty.'


def test_vpn_id():
    """Ensure each VPN has an ID."""
    for v in vpns:
        assert len(v.id) > 0


def test_vpn_details():
    """Ensure that details() returns something."""
    for v in vpns:
        assert len(v.details()) > 0


def test_vpn_string_conversion():
    """Ensure string conversion works."""
    for v in vpns:
        assert len(str(v)) > 0
