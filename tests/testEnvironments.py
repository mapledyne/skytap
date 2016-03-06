"""Test Skytap Environments API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa

environments = Environments()


def test_do_some_environments_exist():
    """Check to see if we have some environments returned."""
    assert len(environments) > 0


def test_svm_count():
    """Ensure our SVM count seems correct."""
    assert environments.svms() > 0
    count = 0
    for l in list(environments.data):
        e = environments[l]
        count += e.svms
    msg = ('SVM count mismatch. Environments says: ' +
           str(environments.svms()) +
           ', actual count: ' + str(count))
    assert count == environments.svms(), msg


def test_vm_count():
    """Ensure our VMs seem correct."""
    assert environments.vm_count() > 0, 'Total VM count should be over 1.'
    count = 0
    for l in list(environments.data):
        e = environments[l]
        count += e.vm_count
    msg = ('VM count mismatch. Environments says: ' +
           str(environments.vm_count()) +
           ', actual count: ' + str(count))
    assert count == environments.vm_count(), msg


def test_svm_vs_vm_count():
    """Make sure svm count is greater than vm count."""
    assert environments.svms() >= environments.vm_count()


def test_environment_id():
    """Ensure environments have ids."""
    for l in list(environments.data):
        e = environments[l]
        assert e.id > 0


def test_environment_details():
    """Ensure environments have details."""
    for l in list(environments.data):
        e = environments[l]
        assert len(e.details()) > 0


def test_environment_str_conversion():
    """Ensure environment str converion works."""
    for l in list(environments.data):
        e = environments[l]
        assert str(e) == e.name
