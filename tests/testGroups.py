import json
import nose
import os
import sys
import uuid

sys.path.append('..')
from skytap.Groups import Groups  # noqa
from skytap.Users import Users  # noqa
groups = Groups()


def group_list_count():
    """Ensure we have some groups.

    This is run by test_group_creation to guarantee that we have
    at least one group there - that function creates a test group.
    """
    assert len(groups) > 0


def test_group_id():
    """Ensure user has id."""
    for l in list(groups.data):
        g = groups[l]
        assert g.id > 0


def test_user_json():
    """Ensure user json conversion seems to be working."""
    for l in list(groups.data):
        g = groups[l]
        assert len(json.dumps(g.json())) > 0


def test_user_count_matches():
    """Make sure the user list counts match.

    Groups come in with a user_count and a list of users. Make sure these
    match.
    """
    for l in list(groups.data):
        g = groups[l]
        msg = ('Checking group ' + str(g.id) + ': ' + g.name + ' ['
               'Reported: ' + str(g.user_count) + ', '
               'Actual: ' + str(len(g.users)) + ']')
    # Bug in Skytap API = this assert will regularly fail. Working with Skytap
    # to correct their API. Leaving commented out until they sort the problem.
    #    assert g.user_count == len(g.users), msg


def test_group_str_conversion():
    """Ensure user string conversion works."""
    for l in list(groups.data):
        g = groups[l]
        assert len(str(g)) > 0


def test_group_module_main():
    ret = json.loads(groups.main([]))
    assert len(ret) == len(groups.data)


def group_main_good_group():
    """Does running this via main() return the expected result.

    This is run by test_group_creation to guarantee that we have
    at least one group there - that function creates a test group.
    """
    assert len(groups.data) > 0, "No groups found to test against."
    group = list(groups.data)[0]
    ret = json.loads(groups.main([groups[group].id]))
    assert groups[group].id == ret[0]['id']


def test_group_main_bad_group():
    group = 'not a group'
    ret = json.loads(groups.main([group]))
    assert len(ret) == 0


def test_group_creation():
    """Create, modify, and delete a group."""
    name = str(uuid.uuid4())
    description = 'Group creation test.'
    group = groups.add(name, description)

    # Run these from inside this test since we can now
    # assume we have some actual group(s) to test:
    group_list_count()
    group_main_good_group()

    assert groups[group].name == name
    user = Users().first()
    msg = 'User (' + user.name + ') not successfully added.'
    assert groups[group].add_user(user.id), msg
    msg = 'User (' + user.name + ') not found after added to group.'
    assert user.id in groups[group].users, msg
    msg = 'User (' + user.name + ') not successfully removed.'
    assert groups[group].remove_user(user.id), msg
    msg = 'User (' + user.name + ') still in group after being removed.'
    remove_invalid_user(group)
    assert user not in groups[group].users, msg
    msg = 'Group (' + name + ') not successfully deleted.'
    assert groups.delete(groups[group]), msg
    access_deleted_group(group)


@nose.tools.raises(TypeError)
def remove_invalid_user(group):
    groups[group].remove_user("string")


@nose.tools.raises(KeyError)
def access_deleted_group(group):
    det = groups[group].name
