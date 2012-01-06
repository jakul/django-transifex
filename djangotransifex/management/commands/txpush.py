"""
txpush.py

Push source translations to transifex.
"""

from django.core.management.base import NoArgsCommand
import app_settings
from djangotransifex.api import DjangoTransifexAPI


class Command(NoArgsCommand):    
    help = 'Push source translations to the Transifex server'
    
    ## Settings ##
    project_slug = app_settings.PROJECT_SLUG
    resource_prefix = app_settings.RESOURCE_PREFIX
    source_language = app_settings.SOURCE_LANGUAGE_CODE
    username = app_settings.TRANSIFEX_USERNAME
    password = app_settings.TRANSIFEX_PASSWORD
    host = app_settings.TRANSIFEX_HOST
    
    @property
    def api(self):
        """
        Create an api instance
        """
        if not hasattr(self, '_api'):
            self._api = DjangoTransifexAPI(
                username=self.username, password=self.password, host=self.host
            )
            #TODO: Do a ping here
        return self._api
    
    def handle_noargs(self, **options):
        self.api.upload_source_translations(project_slug=self.project_slug)
        
