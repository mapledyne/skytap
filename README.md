skynet v3.0
======

Skynet is an extensible set of functions that we use to manage many aspects of our Skytap infrastructure.

## What is inside:
 - **skynet.py** -- This is the script that does all the work
 - **exclude.sh** -- a bash script for the time being.  It takes the contents of the skytap-control directory and manipulates it into a usable form, for input to skynet.py.  Primarily it allows folks to specify exclusions to suspend procedures.  This will one day be pythonized.
 - **config_template.yml** -- This is a configuration example.  The real config file must be at config.yml, and you need to create it.
 - **README.md** -- this file
 - **LICENSE.md** -- Licensing information