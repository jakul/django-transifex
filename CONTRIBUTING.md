## Testing

To run the tests, clone the repository, and then:

    # Setup the virtual environment
    virtualenv env
    env/bin/activate
    pip install -r requirements.txt

    # Run the tests
    py.test

You can also use the excellent [`tox`][tox] testing tool to run the tests against all supported versions of Python and Django.  Install `tox` globally, and then simply run:

    tox
