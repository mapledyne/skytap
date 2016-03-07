import json
import nose
import os
import sys
import uuid

sys.path.append('..')
from skytap.Users import Users  # noqa

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


def test_user_json():
    """Ensure environment json conversion seems to be working."""
    for l in list(users.data):
        u = users[l]
        assert len(json.dumps(u.json())) > 0


def test_user_str_conversion():
    """Ensure user string conversion works."""
    for u in users:
        assert len(str(u)) > 0


def test_user_creation():
    """Create, modify, and delete a user."""
    transfer_to = users.first()
    email = str(uuid.uuid4()) + '@example.com'
    user = users.add(email)
    assert user > 0
    assert users[user].email == email

    assert users.delete(user, transfer_to)
    access_deleted_user(user)


@nose.tools.raises(KeyError)
def access_deleted_user(user):
    det = users[user]


def test_user_module_main():
    """Ensure we get something when running the main function."""
    ret = json.loads(users.main([]))
    assert len(ret) == len(users.data)


def test_user_main_good_user():
    """Ensure searching for a user id returns that ID."""
    user = list(users.data)[0]
    ret = json.loads(users.main([users[user].id]))
    assert users[user].id == ret[0]['id']


def test_user_main_bad_user():
    """Ensure searching for a non-existant user doesn't find anything."""
    user = 'not a user'
    ret = json.loads(users.main([user]))
    assert len(ret) == 0
