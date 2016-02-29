"""Skytap API object wrapping Skytap templates.

This roughly translates to the Skytap API call of /v2/templates REST call,
but gives us better access to the bits and pieces of the templates.

If accessed via the command line (``python -m skytap.Templates()``) this will
return the templates from Skytap in a JSON format.
"""
from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Template import Template
import sys


class Templates(SkytapGroup):

    """Set of Skytap templates.

    :Example:
    >>> t = skytap.Templates()
    >>> print len(t)
    12
    """

    def __init__(self):
        """Build an initial list of templates."""
        super(Templates, self).__init__()
        self.load_list_from_api('/v2/templates', Template)

    def vm_count(self):
        """Count the total number of VMs."""
        count = 0
        for e in self.data:
            count += self.data[e].vm_count
        return count

    def svms(self):
        """Count the total number of SVMs in use."""
        count = 0
        for e in self.data:
            count += self.data[e].svms
        return count

    def storage(self):
        """Count the total amount of storage in use."""
        count = 0
        for e in self.data:
            count += self.data[e].storage
        return count

if __name__ == '__main__':
    print(Templates().main(sys.argv[1:]))
