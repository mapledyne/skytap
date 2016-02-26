"""Skytap API object wrapping Skytap Environments.

This roughly translates to the Skytap API call of /v2/configurations REST call,
but gives us better access to the bits and pieces of the environments.

If accessed via the command line (``python -m skytap.Environments()``)
this will return the environments from Skytap in a JSON format.
"""
import json
from skytap.models.Environment import Environment
from skytap.models.SkytapGroup import SkytapGroup


class Environments(SkytapGroup):

    """Set of Skytap environments.

    :Example:
    >>> envs = skytap.Environments()
    >>> print len(envs)
    42
    """

    def __init__(self):
        """Build an initial list of environments."""
        super(Environments, self).__init__()
        self.load_list_from_api('/v2/configurations',
                                Environment,
                                {'scope': 'company'})

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

    def delete(self, env):
        """Delete a given environment."""
        if isinstance(env, Environment):
            if env.id not in self.data:
                raise KeyError
            env.delete()
        elif isinstance(env, int):
            if env not in self.data:
                raise KeyError
            self.data[env].delete()
        else:
            raise KeyError
        self.refresh()

if __name__ == '__main__':
    envs = Environments()
    print(json.dumps(envs.json, indent=4))
