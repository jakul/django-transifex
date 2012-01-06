from django.conf import settings

#project_slug = settings.TRANSIFEX_PROJECT_NAME
#resource_prefix = 'aproject'#TRANSIFEX_RESOURCE_PREFIX
#source_language = settings.LANGUAGE_CODE
#username = settings.TRANSIFEX_USERNAME
#password = settings.TRANSIFEX_PASSWORD
#host = settings.TRANSIFEX_HOST

TRANSIFEX_USERNAME = getattr(settings, 'TRANSIFEX_USERNAME')
TRANSIFEX_PASSWORD = getattr(settings, 'TRANSIFEX_PASSWORD')
TRANSIFEX_HOST = getattr(settings, 'TRANSIFEX_HOST', 'https://www.transifex.net/')
SOURCE_LANGUAGE_CODE = getattr(settings, 'TRANSIFEX_SOURCE_LANGUAGE', settings.LANGUAGE_CODE)
RESOURCE_PREFIX = getattr(settings, 'TRANSIFEX_RESOURCE_PREFIX', '')
PROJECT_SLUG = getattr(settings, 'TRANSIFEX_PROJECT_SLUG', 'MyProject')

def _get_project_path():
    from django.utils.importlib import import_module
    import os
    parts = settings.SETTINGS_MODULE.split('.')
    project = import_module(parts[0])
    projectpath = os.path.abspath(os.path.dirname(project.__file__))
    return projectpath

# Not strictly a setting, but this is a good place to keep it
PROJECT_PATH = _get_project_path()
