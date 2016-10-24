"""Support for Skytap API access to the company quotas.

If accessed via the command line (``python -m skytap.Quotas``) this will
return the quotas from Skytap in a JSON format.
"""
import json
import sys

from skytap.models.Quota import Quota
from skytap.models.SkytapGroup import SkytapGroup


class Quotas(SkytapGroup):
    """Company/account quotas object."""

    def __init__(self):
        """Load the quotas from Skytap."""
        super(Quotas, self).__init__()
        quota_rest = self.rest('/v2/company/quotas')
        quota_json = json.loads(quota_rest)
        for qu in quota_json:
            print(quota_json[qu][0])
        q = Quota(quota_json["US-West"][0])


if __name__ == '__main__':
    print(Quotas().main(sys.argv[1:]))
