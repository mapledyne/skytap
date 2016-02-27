import json
import os
import sys

sys.path.append('..')
from skytap.Users import Users  # nopep8

users = Users()


def test_user_list():
    """Ensure we have some users."""
    assert len(users) > 0, 'User list is empty.'


def test_user_admins():
    """Ensure we have at least one admin."""
    assert users.admins() > 0


def test_user_id():
    """Ensure user has id."""
    for u in users:
        assert u.id > 0


def test_user_details():
    """Ensure user has details()."""
    for u in users:
        assert len(u.details()) > 0


def test_user_str_conversion():
    """Ensure user string conversion works."""
    for u in users:
        assert len(str(u)) > 0


def test_user_module_main():
    ret = json.loads(users.main([]))
    assert len(ret) == len(users.data)


def test_user_main_good_user():
    user = list(users.data)[0]
    ret = json.loads(users.main(['', users[user].id]))
    assert users[user].id == ret['id']


def test_user_main_bad_user():
    user = 'not a user'
    ret = json.loads(users.main(['', user]))
    assert 'error' in ret
