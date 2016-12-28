"""Skytap API object wrapping Skytap Export Jobs.

This roughly translates to the Skytap API call of /v2/exports REST call,
but gives us better access to the bits and pieces of the VPN.

If accessed via the command line (``python -m skytap.Exports``) this will
return a list of current Exports from Skytap in a JSON format.
"""
import sys

from skytap.models.SkytapGroup import SkytapGroup
from skytap.models.Export import Export


class Exports(SkytapGroup):
    """Set of Skytap Export Jobs.

    Example:
        exports = skytap.Exports()
        print len(exports)
    """

    def __init__(self):
        """Build the Export list from the Skytap API."""
        super(Exports, self).__init__()
        self.load_list_from_api('/v2/exports', Export)

    def delete(self, job):

        target_id = job.id
        if isinstance(job, Export):
            if target_id not in self.data:
                raise KeyError
            job.delete()
        elif isinstance(job, int):
            if job not in self.data:
                raise KeyError
            self.data[job].delete()
        else:
            raise KeyError
        self.refresh()
        return target_id not in self.data


if __name__ == '__main__':
    print(Exports().main(sys.argv[1:]))
