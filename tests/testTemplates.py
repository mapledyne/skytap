"""Test Skytap Templates API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Templates import Templates  # nopep8


class TestTemplates(object):

    """Unittest class to test the Templates."""

    def setUp(self):
        """Build the environment set we want to test with."""
        self.templates = Templates()

    def test_do_some_templates_exist(self):
        """Check to see if we have some templates returned."""
        assert len(self.templates) > 0

    def test_svm_count(self):
        """Ensure our SVMs over 0."""
        assert self.templates.svms() > 0

    def test_vm_count(self):
        """Ensure our VMs over 0."""
        assert self.templates.vm_count() > 0

    def test_svm_vs_vm_count(self):
        """Make sure svm count is greater than vm count."""
        assert self.templates.svms() >= self.templates.vm_count()

    def test_template_ids(self):
        """Verifying template ids."""
        for t in self.templates:
            assert t.id > 0, 'No template ID found'

    def test_template_details(self):
        """Test to ensure details() returns something."""
        for t in self.templates:
            assert len(t.details()) > 0, tmp.name + ': No details found'

    def test_template_name(self):
        """Test that the template name has something."""
        for t in self.templates:
            assert len(t.name) > 0, str(tmp.id) + ': No name found'

    def test_template_str_conversion(self):
        """Test string conversion."""
        for t in self.templates:
            assert len(str(t)) > 0, tmp.name + ': string conversion error'
