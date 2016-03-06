import json
import os
import sys

sys.path.append('..')
from skytap.models.Environment import Environment  # noqa
from skytap.models.SkytapGroup import SkytapGroup  # noqa
from skytap.models.SkytapResource import SkytapResource  # noqa


class SkytapGroupToTest(SkytapGroup):
    def __init__(self):
        super(SkytapGroupToTest, self).__init__()
        self.load_list_from_api('/v2/configurations', SkytapResourceToTest)


class SkytapResourceToTest(SkytapResource):
    def __init__(self, test_json):
        super(SkytapResourceToTest, self).__init__(test_json)

group = SkytapGroupToTest()
resource = group.first()


def test_read_details():
    """Ensure we get something from details()."""
    assert len(resource.details()) > 0


def test_has_id():
    """Ensure we have an ID."""
    assert 'id' in resource


def test_int_conversion():
    """Ensure we can convert to an int."""
    assert resource.id == int(resource)


def test_hash():
    """Test hashing functions."""
    hsh = hash(resource)


def test_equality():
    """Test equality."""
    assert resource == resource


def test_gt_lt():
    """Test greater and less than."""
    assert resource > 0
    assert resource < 1000000000


def test_contains():
    """Make sure 'contains' works."""
    assert 'id' in resource
    assert 'this_should_not_exist' not in resource
