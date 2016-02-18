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
        "title": "Master of Ceremonies",
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

Put all the files in a directory. Edit the config.yml to if there are changes to behavior you'd like.

The config will also pull variables from your environment variables, matching anything in the config.yml. This allows you to specify your Skytap API token via the environment variable "SKYTAP_TOKEN" instead of putting it in the config file (it will replace the "token" variable from the config). It's very recommended you expose the user ("SKYTAP_USER") and token in this way, instead of putting those values in the config.yml file.

The easiest way to do this is to create a `.skytap` file in your home (`~/.skytap`) and source the file from your `.bash_profile` or similar file.

For instance, add a line in your `~/.bash_profile`:

    source ~/.skytap

Then, create a new file called `~/.skytap` with the following:

    export SKYTAP_USER=kermit.frog@fulcrum.net
    export SKYTAP_TOKEN=22afe22616dab53a6773733be273fe7a663b4

This will protect your user and token information from someone reading the config file separately, and make it easier to share your config or script changes without fear of exposing your API token.

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
