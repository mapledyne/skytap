"""Support for Skytap API access to the company quotas.

If accessed via the command line (``python -m skytap.Quotas``) this will
return the quotas from Skytap in a JSON format.
"""
from skytap.models.Quota import Quota
from skytap.models.SkytapGroup import SkytapGroup
import sys


class Quotas(SkytapGroup):

    """Company/account quotas object."""

    def __init__(self):
        """Load the quotas from Skytap."""
        super(Quotas, self).__init__()
        self.load_list_from_api('/v2/company/quotas', Quota)

if __name__ == '__main__':
    print(Quotas().main(sys.argv[1:]))
