

Settings
========
You must set the following in your settings file

    TRANSIFEX_USERNAME = # The username for the transidex server
    TRANSIFEX_PASSWORD # The password for the transifex server

The following are optional settings


    TRANSIFEX_HOST # The transifex host to use
                   # default: `https://www.transifex.net/`
    SOURCE_LANGUAGE_CODE # The source language for your strings.
                         # default: The Django LANGUAGE_CODE setting
    RESOURCE_PREFIX # What prefix to give the resources
                    # default: No prefix
    PROJECT_SLUG # The slug for the project
                 # default: `MyProject`
    LANGUAGE_MAPPING: # A set of key/value mappings, where the key is the
                      # Transifex language code, and the value is the
                      # Django language code
                      # default: No mappings


CHANGELOG
=========

0.1.4
-----
* Make the user confirm their intentions when they are pushing translations which could destroy work done
  on the Transifex server

0.1.3
-----
* Add output on commandline when commands execute sucessfully
* Add example settings into readme

