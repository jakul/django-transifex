Djangotransifex
===============

This app can help you push/pull *project level* translations into Transifex.

Settings
========
You must set the following in your settings file

    # The username for the Transifex server
    TRANSIFEX_USERNAME = 'username'
    
    # The password for the Transifex server
    TRANSIFEX_PASSWORD = 'password'


The following are optional settings


    # The Transifex host to use
    # default: `https://www.Transifex.net/`
    TRANSIFEX_HOST
    
    # The source language for your strings.
    # default: The Django LANGUAGE_CODE setting
    SOURCE_LANGUAGE_CODE
    
    # What prefix to give the resources
    # default: No prefix
    RESOURCE_PREFIX
    
    # The slug for the project
    # default: `MyProject`
    PROJECT_SLUG
    
    # A set of key/value mappings, where the key is the
    # Transifex language code, and the value is the
    # Django language code
    # default: No mappings
    LANGUAGE_MAPPING


CHANGELOG
=========

0.1.10
------
* Relax requirements versions

0.1.9
-----
Fix pypi version

0.1.8
-----
* Swtich to py.test and tox.ini

0.1.7
-----
* Make `PROJECT_PATH` setting overridable from `settings.py`
* Convert `README.rst` to be markdown

0.1.6
-----
* Make pull_translations and create_project commands print to the command line

0.1.5
-----
* Output the name of the command being run before the command executes
* Make the user confirm on update_source_translations, as it is a destructive action

0.1.4
-----
* Make the user confirm their intentions when they are pushing translations which could destroy work done
  on the Transifex server

0.1.3
-----
* Add output on commandline when commands execute sucessfully
* Add example settings into readme

