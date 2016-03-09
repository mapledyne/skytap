"""Test Skytap Environments API access."""
import json
import os
import sys
import time
import uuid

sys.path.append('..')
from skytap.Environments import Environments  # noqa

environments = Environments()
notes_to_check = 25

testing_env = None
testing_vm = None


def setUp():
    global testing_env, testing_vm
    if testing_env is not None and testing_vm is not None:
        return
    for e in list(environments.data):
        if testing_env is not None and testing_vm is not None:
            break
        if testing_env is None:
            if len(environments[e].notes) == 0:
                testing_env = environments[e]
        for v in list(environments[e].vms.data):
            if testing_vm is not None:
                break
            if len(environments[e].vms[v].notes) == 0:
                testing_vm = environments[e].vms[v]
    assert testing_env is not None, 'No suitable testing environment found.'
    assert testing_vm is not None, 'No suitable testing VM found.'


def tearDown():
    testing_env.notes.delete_all()
    testing_vm.notes.delete_all()


def test_note_manipulation():
    """Create and delete a note."""
    msg = str(uuid.uuid4())
    count = len(testing_env.notes)
    testing_env.notes.add(msg)
    note = testing_env.notes.newest()

    assert len(testing_env.notes) == count + 1

    assert note.id > 0, 'No note ID found.'
    assert len(note.text) > 0, "Note [" + str(note.id) + "] empty."
    assert note.text == str(note), "Note [" + str(note.id) + "] mismatching."
    assert note.text == msg

    assert note.created_at <= note.updated_at, ("Note [" + str(note.id) +
                                                "] updated before it was " +
                                                "created.")

    older = note
    time.sleep(2)
    testing_env.notes.add(str(uuid.uuid4()))
    assert testing_env.notes.oldest() > testing_env.notes.newest()
    testing_env.notes.delete_all()
    assert len(testing_env.notes) == 0
