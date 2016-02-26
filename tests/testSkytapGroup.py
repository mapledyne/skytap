import json
import os
import sys

sys.path.append('..')
from skytap.models.Environment import Environment  # nopep8
from skytap.models.SkytapGroup import SkytapGroup  # nopep8


class SkytapGroupToTest(SkytapGroup):
    def __init__(self):
        super(SkytapGroupToTest, self).__init__()

group = SkytapGroupToTest()


def test_load_from_api():
    group.load_list_from_api('/v2/configurations', Environment)


def test_load_from_api_with_parameter():
    group.load_list_from_api('/v2/configurations',
                             Environment, {'scope': 'company'})
