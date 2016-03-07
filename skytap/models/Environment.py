"""Support for an Environment resource in Skytap.

In nearly every case, you'll access an Environment via the
:class:`~skytap.Environments` object::

    envs = skytap.Environments()
    for environment in envs:
        print (environment.name)

You can access anything from an environment that Skytap includes in their
`API <http://help.skytap.com/#API_v2_Documentation.html#Environm>`_.
Most of these can be access directly as attributes of the given
Environment object::

    environment = skytap.Environments()[12345]
    print(environment.name)
    print(environment.json)

Some data conversions are handled for you. Specifically:

* Dates are converted into :class:`datetime` objects, like :attr:`created_at`.
* The :attr:`vms` list is loaded into a :class:`skytap.models.Vms` class.
* The :attr:`notes`, if loaded, are put into a :class:`skytap.models.Notes` class.
* The :attr:`user_data`, if loaded, is put into a :class:`skytap.models.UserData` class.


There's also the ability to change the runstate of the environment through
the function :func:`change_state`::

    environment = skytap.Environments()[12345]
    environment.change_state('suspended')

    # Passing `True` will wait for the suspend to complete
    # before returning to the script:
    environment.change_state('suspended', True)

The various state change options also have easy aliases available to them:

* :func:`run()`
* :func:`halt()`
* :func:`suspend()`
* :func:`reset()`
* :func:`stop()`

Passing `True` to any of these will also cause the script to wait until
the action is completed by Skytap.

.. note::
    Some pieces of a given environment, specifically `notes` and `user_data`,
    are only available via additional calls to the API. These fields will
    not exist when first creating the environments object, but any direct
    access to those fields will trigger the API call behind the scenes.

    This is important if you're listing the entire contents (say, sending it
    to a JSON) - these fields won't be included if you haven't made that direct
    access.

    This is by design to conserve API calls as most usage doesn't need or use
    those fields.
"""
import json

from skytap.framework.ApiClient import ApiClient
from skytap.framework.Suspendable import Suspendable
import skytap.framework.Utils as Utils
from skytap.models.Notes import Notes
from skytap.models.SkytapResource import SkytapResource
from skytap.models.UserData import UserData
from skytap.models.Vms import Vms


class Environment(SkytapResource, Suspendable):

    """One Skytap environment."""

    def __init__(self, env_json):
        """Init is mainly handled by the parent class."""
        super(Environment, self).__init__(env_json)

    def _calculate_custom_data(self):
        """Add custom data.

        Specifically, boolean values to more easily determine state, allowing
        things like 'if env.running:' to be used.
        """
        self.data['running'] = self.runstate == 'running'
        self.data['busy'] = self.runstate == 'busy'
        self.data['suspended'] = self.runstate == 'suspended'
        self.data['vms'] = Vms(self.vms, self.id)

    def __getattr__(self, key):
        """Load values for anything that doesn't get loaded by default.

        For user_data and notes, a secondary API call is needed. Only make that
        call when the info is requested.
        """
        if key == 'user_data':
            if key in self.data:
                return self.data[key]
            api = ApiClient()
            user_json = api.rest(self.url + '/user_data.json')
            self.data['user_data'] = UserData(json.loads(user_json), self.url)
            return self.user_data

        if key == 'notes':
            api = ApiClient()
            notes_json = api.rest(self.url + '/notes.json')
            self.notes = Notes(notes_json, self.url)
            return self.notes

        return super(Environment, self).__getattr__(key)

    def delete(self):
        """Delete the environment.

        In general, it'd seem wise not to do this very often.
        """
        Utils.info('Deleting environment: ' +
                   str(self.id) + '(' + self.name + ')')
        api = ApiClient()
        response = api.rest(self.url_v1,
                            {},
                            'DELETE')
        return response
