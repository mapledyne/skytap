import json
import os
import sys

sys.path.append('..')
from skytap.Quotas import Quotas  # noqa

quotas = Quotas()


def test_quota_count():
    assert len(quotas) > 0


def test_quota_id():
    for quota in quotas:
        assert len(quota.id) > 0


def test_quota_usage():
    for quota in quotas:
        assert quota.usage >= 0


def test_quota_units():
    for quota in quotas:
        assert len(quota.units) > 0


def test_quota_limit():
    for quota in quotas:
        if quota.limit is not None:
            assert quota.usage <= quota.limit
            assert quota.pct == quota.usage * 100.0 / quota.limit


def test_quota_time():
    for quota in quotas:
        if quota.units == 'hours':
            assert quota.time.seconds > 0


def test_quota_str_conversion():
    for quota in quotas:
        assert len(str(quota)) > 0
