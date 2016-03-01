"""Skytap API object wrapping Skytap Environments.

This roughly translates to the Skytap API call of /v2/configurations REST call,
but gives us better access to the bits and pieces of the environments.

Accessing via command line
==========================

If accessed via the command line this will return the environments from
Skytap in a JSON format::

    python -m skytap.Environments

If you know the environment you want information on, you can also specify
it directly. You can search by id or by a part of the environment name::

    python -m skytap.Environments 12345
    python -m skytap.Environments test

Additionally, you can search on some other crieria of a group to get a set
you're looking for.

Runstate::

    python -m skytap.Environments running  # or 'suspended',
        'stopped', or 'busy'

Region::

    python -m skytap.Environments us-west

Accessing via Python
====================

After you've installed ``skytap`` and added ``import skytap`` to your
script, you can access the Skytap environments by the
:class:`skytap.Environments` object.

Example:
    >>> envs = skytap.Environments()
    >>> for e in envs:
    >>>     print(e.name)

Each environment has many things you can do with it - see the
:class:`skytap.models.Environment` object for actions you can take on an
individual environment.

On the full list of environments, you can also get a vm count, svm count,
get global storage, and delete environments. Each action is documented, below.

Environments can also perform any of the actions of other
:class:`SkytapGroup` objects. See the documentation
on the :class:`skytap.models.SkytapGroup` class for
information there.
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
        self.search_fields.append('runstate')
        self.search_fields.append('region')

    def vm_count(self):
        """Count the total number of VMs.

        Returns:
            int: Number of VMs used across all environments.

        Example:
            >>> envs = skytap.Environments()
            >>> print(envs.vm_count())
            112
        """
        count = 0
        for e in self.data:
            count += self.data[e].vm_count
        return count

    def svms(self):
        """Count the total number of SVMs in use.

        Returns:
            int: Number of SVMs used across all environments.

        Example:
            >>> envs = skytap.Environments()
            >>> print(envs.svms())
            312
        """
        count = 0
        for e in self.data:
            count += self.data[e].svms
        return count

    def storage(self):
        """Count the total amount of storage in use.

        Returns:
            int: Amount of storage used across all environments.

        Example:
            >>> envs = skytap.Environments()
            >>> print(envs.storage()))
            57229376
        """
        count = 0
        for e in list(self.data):
            count += self.data[e].storage
        return count

    def delete(self, env):
        """Delete a given environment.

        .. warning::
            This is unrecoverable. Use with **extreme** caution.

        Args:
            env (Environment): The environment to delete.

        Returns:
            bool: True if the environment was deleted.
        Raises:
            KeyError: If ``env`` isn't in the Environments set.

        Example:
            >>> envs = skytap.Environments()
            >>> target = envs[12345]
            >>> envs.delete(target)
            True
        """
        target_id = env.id
        if isinstance(env, Environment):
            if target_id not in self.data:
                raise KeyError
            env.delete()
        elif isinstance(env, int):
            if env not in self.data:
                raise KeyError
            self.data[env].delete()
        else:
            raise KeyError
        self.refresh()
        return target_id not in self.data

if __name__ == '__main__':
    print(Environments().main(sys.argv[1:]))
