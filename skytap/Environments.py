"""Skytap API object wrapping Skytap Environments.

This roughly translates to the Skytap API call of /v2/configurations REST call,
but gives us better access to the bits and pieces of the environments.

If accessed via the command line this will return the environments from
Skytap in a JSON format.

Example:
    ``python -m skytap.Environments``

Accessing via python is also easy.

Example:
    >>> envs = skytap.Environments()
    >>> for e in envs:
    >>>     print(e.name)
"""
from skytap.models.Environment import Environment
from skytap.models.SkytapGroup import SkytapGroup
import sys


class Environments(SkytapGroup):

    """Set of Skytap environments."""

    def __init__(self):
        """Build an initial list of environments."""
        super(Environments, self).__init__()
        self.load_list_from_api('/v2/configurations',
                                Environment,
                                {'scope': 'company'})

    def vm_count(self):
        """Count the total number of VMs.

        Returns:
            int: Number of VMs used across all environments.
        """
        count = 0
        for e in self.data:
            count += self.data[e].vm_count
        return count

    def svms(self):
        """Count the total number of SVMs in use.

        Returns:
            int: Number of SVMs used across all environments.
        """
        count = 0
        for e in self.data:
            count += self.data[e].svms
        return count

    def storage(self):
        """Count the total amount of storage in use.

        Returns:
            int: Amount of storage used across all environments.
        """
        count = 0
        for e in self.data:
            count += self.data[e].storage
        return count

    def delete(self, env):
        """Delete a given environment.

        .. warning::
            This is unrecoverable. Use with **extreme** caution.

        Args:
            env (Environment): The environment to delete.

        Raises:
            KeyError: If ``env`` isn't in the Environments set.
        """
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
    print(Environments().main(sys.argv[1:]))
