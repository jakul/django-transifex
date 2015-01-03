def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        ROOT_URLCONF='tests.urls',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'djangotransifex',
            'tests',
        ),
        TRANSIFEX_USERNAME = 'abcde',
        TRANSIFEX_PASSWORD = 'abcde',
        TRANSIFEX_LANGUAGE_MAPPING = {'en_GB': 'en-gb', 'it_IT': 'it'},
        LANGUAGE_CODE = 'en-gb',
        LANGUAGES = (('en-gb', 'English'), ('it', 'Italian')),
        TRANSIFEX_PROJECT_PATH = '.'
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
