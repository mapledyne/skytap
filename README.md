skynet
======

Skynet is an extensible set of functions that we use to manage aspects of our Skytap infrastructure here at [Fulcrum Technologies](http://fulcrum.net).

We made this to be easily extensible so we can quickly make use of other pieces of the Skytap API.

## Usage

To use skynet, run the skynet script with some sort of action:

    python skynet.py -a users

You'll get back a JSON for the request, something like:

    [
      {
        "id": "12345",
        "url": "https://cloud.skytap.com/users/12345",
        "login_name": "kermit.frog@fulcrum.net",
        "first_name": "Kermit",
        "last_name": "The Frog",
        "title": "",
        "email": "kermit.frog@fulcrum.net",
        "created_at": "2012-01-02T12:43:05-08:00",
        "deleted": false
      }
    ]

To get a list of actions, run it without any parameters:

    python skynet.py

Or get help on an action by using:

    python skynet.py -h users


## Installation

Put all the files in a directory, then copy the `config_template.yml` file and rename the new file `config.yml`. There are a few variables you need to put in there to get the system configured, like the API key. Comments are in the file.

## New actions

The design of Skynet is to be quickly extensible, so as a part of that we heavily leverage Docstrings and similar features of Python. This results in a new action being able to be added simply by creating a new function in the `skynet_actions.py` file.

For instance, when Skytap starts offering jokes via their API, this can be added like this:

    def joke(user_id):
        """Get a user's joke.

        Get's the joke tied to this user's account.
        """
        return _api.rest('/joke/' + user_id)

And that's it. The `skynet.py` will see the function and add it to the list of actions in its help, and the docstrings are accessible both via the action list (calling `skynet.py` with no parameters) and via full help (`skynet.py -h joke`).

The `_api` module is from the `skytap_api.py` file, which wraps the Skytap API itself. It then knows the URL and rest of the info needed to get to the API, so you can use `_api.rest()` or `_api.post()` as desired. The string sent should either look like `'/users'` or, for the v2 API, like `'/v2/configurations'`

## Contributor list:
* Bill Wellington [github](https://github.com/thewellington/) [twitter]() [blog](http://www.wellingtonnet.net)
* Michael Knowles [github](https://github.com/mapledyne) [twitter]() [blog](http://mapledyne.com)
* Caleb Hawkins [github](https://github.com/calebh93) [twitter](https://twitter.com/MuddyTM)

Contact us directly for questions, or you can reach Fulcrum Technologies on [Twitter](https://twitter.com/lifeatfulcrum).
