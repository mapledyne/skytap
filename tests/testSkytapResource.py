import json
import os
import sys

sys.path.append('..')
from skytap.models.Environment import Environment  # nopep8
from skytap.models.SkytapGroup import SkytapGroup  # nopep8
from skytap.models.SkytapResource import SkytapResource  # nopep8


class SkytapGroupToTest(SkytapGroup):
    def __init__(self):
        super(SkytapGroupToTest, self).__init__()
        self.load_list_from_api('/v2/configurations', SkytapResourceToTest)


class SkytapResourceToTest(SkytapResource):
    def __init__(self, test_json):
        super(SkytapResourceToTest, self).__init__(test_json)


class TestSkytapGroup(object):

    def setUp(self):
        self.group = SkytapGroupToTest()
        self.resource = list(self.group)[0]

    def test_read_details(self):
        """Ensure we get something from details()."""
        assert len(self.resource.details()) > 0

    def test_has_id(self):
        """Ensure we have an ID."""
        assert 'id' in self.resource

    def test_int_conversion(self):
        """Ensure we can convert to an int."""
        assert self.resource.id == int(self.resource)

    def test_hash(self):
        """Test hashing functions."""
        hsh = hash(self.resource)

    def test_equality(self):
        """Test equality."""
        assert self.resource == self.resource

    def test_gt_lt(self):
        """Test greater and less than."""
        assert self.resource > 0
        assert self.resource < 1000000000

    def test_contains(self):
        """Make sure 'contains' works."""
        assert 'id' in self.resource
        assert 'this_should_not_exist' not in self.resource
