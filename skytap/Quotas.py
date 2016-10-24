"""Support for Skytap API access to the company quotas.

If accessed via the command line (``python -m skytap.Quotas``) this will
return the quotas from Skytap in a JSON format.
"""
import json
import sys

from skytap.models.Quota import Quota
from skytap.models.SkytapGroup import SkytapGroup


class Quotas(SkytapGroup):
    """Company/account quotas object.

    Note: This code assumes that you have regional limits on your account.
    The return is different if you don't (see the /v2 API doc). We should get
    each piece of the return and sort it into type-and-region (whether you
    have regional limits or not) and can then access things uniformly. Doing
    so will also require smartly accessing the API on demand more, since
    accounts with regional limits may require multiple calls to get the info
    desired.
    """

    def __init__(self):
        """Load the quotas from Skytap."""
        super(Quotas, self).__init__()
        quota_rest = self.rest('/v2/company/quotas')
        quota_json = json.loads(quota_rest)
        for qu in quota_json:
            self.data[qu] = Quota(quota_json[qu][0])


if __name__ == '__main__':
    print(Quotas().main(sys.argv[1:]))
