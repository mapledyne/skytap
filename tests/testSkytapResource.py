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
        """Do we get some details back?"""
        assert len(self.resource.details()) > 0

    def test_has_id(self):
        """Ensure we have an ID."""
        assert 'id' in self.resource
