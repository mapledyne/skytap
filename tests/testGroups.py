import json
import os
import sys

sys.path.append('..')
from skytap.Groups import Groups  # nopep8

groups = Groups()


def test_group_list():
    """Ensure we have some users."""
    assert len(groups) > 0, 'User list is empty.'


def test_group_id():
    """Ensure user has id."""
    for g in groups:
        assert g.id > 0


def test_user_details():
    """Ensure user has details()."""
    for g in groups:
        assert len(g.details()) > 0


def test_user_count_matches():
    """Make sure the user list counts match.

    Groups come in with a user_count and a list of users. Make sure these
    match.
    """
    for l in list(groups.data):
        g = groups[l]
        msg = ('Checking group: ' + g.name + ' ['
               'Reported: ' + str(g.user_count) + ', '
               'Actual: ' + str(len(g.users)) + ']')
        print(msg)
        assert g.user_count == len(g.users)


def test_group_str_conversion():
    """Ensure user string conversion works."""
    for g in groups:
        assert len(str(g)) > 0


def test_group_module_main():
    ret = json.loads(groups.main([]))
    assert len(ret) == len(groups.data)


def test_group_main_good_group():
    group = list(groups.data)[0]
    ret = json.loads(groups.main(['', groups[group].id]))
    assert groups[group].id == ret['id']


def test_group_main_bad_group():
    group = 'not a group'
    ret = json.loads(groups.main(['', group]))
    assert 'error' in ret
