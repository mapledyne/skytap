"""Test Skytap Templates API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Templates import Templates  # nopep8


templates = Templates()


def test_do_some_templates_exist():
    """Check to see if we have some templates returned."""
    assert len(templates) > 0


def test_svm_count():
    """Ensure our SVMs over 0."""
    assert templates.svms() > 0


def test_vm_count():
    """Ensure our VMs over 0."""
    assert templates.vm_count() > 0


def test_svm_vs_vm_count():
    """Make sure svm count is greater than vm count."""
    assert templates.svms() >= templates.vm_count()


def test_template_ids():
    """Verifying template ids."""
    for t in templates:
        assert t.id > 0


def test_template_details():
    """Test to ensure details() returns something."""
    for t in templates:
        assert len(t.details()) > 0


def test_template_name():
    """Test that the template name has something."""
    for t in templates:
        assert len(t.name) > 0


def test_template_str_conversion():
    """Test string conversion."""
    for t in templates:
        assert len(str(t)) > 0
