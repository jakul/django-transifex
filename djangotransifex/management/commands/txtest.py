"""
Manual tasks:
* setup teams (if not outsourcing them)
* enable 'Fill up resources from TM' (project edit page)
"""

from django.core.management.base import NoArgsCommand
import requests
import json
from transifex.api import TransifexAPI
from transifex.exceptions import TransifexAPIException
from django.conf import settings
import os
import glob
import sys
from clint.textui import colored, indent, puts
import myonzo
from django.template.defaultfilters import slugify
from translation import TRANSIFEX_RESOURCE_PREFIX



class Command(NoArgsCommand):    
#    help = 'Checks the translations for inconsistencies'
#    languages = [
#        code for code,__ in settings.LANGUAGES if code != 'en-gb'
#    ]
#    domains = ['django', 'djangojs']
    #[ord(char) for char in 'abc']
#    host = 'https://www.transifex.net/'
#    base_api_url = 'https://www.transifex.net/api/2'
#    auth = ('jakul', ''.join(chr(num) for num in [98, 117, 110, 110, 121, 49, 50, 51, 65, 100]))
#    
#    project_with_good_teams = 'sandbox'
#    project_name = 'aproject'
#    resources = ['django.po',]#, 'djangojs.po', 'models.po']

    ## Settings ##
    project_slug = settings.TRANSIFEX_PROJECT_NAME
    resource_prefix = TRANSIFEX_RESOURCE_PREFIX
    source_language = settings.LANGUAGE_CODE
    languages = [
        code for code, __ in settings.LANGUAGES if code != source_language
    ]
    username = settings.TRANSIFEX_USERNAME
    password = settings.TRANSIFEX_PASSWORD
    host = settings.TRANSIFEX_HOST
    
    
    def handle_noargs(self, **opts):
        """
        
        @param resource_prefix optional
            The resource prefix to use. Default is the project version number,
            or the string 'dev' for dev machines
        """
        # TODO: override resource prefix
        # TODO: override resource username
        # TODO: override resource password
        # TODO: override resource host
        # TODO: only pull 1 language
        # TODO: only pull 1 resource
        self.api = TransifexAPI(
            username=self.username, password=self.password, host=self.host
        )
#        print self.api.list_resources('aproject')
#        print [o['slug'] for o in self.api.list_resources('aproject')]
#        import pdb
#        pdb.set_trace()
        
        
        #self.resource_prefix = '1_9_9_'
        self.upload_source_translation()
        return
    
    
    def upload_source_translation(self):
        """
        Uploads the current translations as a new source translations. Uses
        settings.LANGUAGE_CODE as the source language code.
        
        This command will create resources if they don't already exist
        """
        source_folder = os.path.join(
             settings.OUR_ROOT, 'locale', settings.LANGUAGE_CODE, 'LC_MESSAGES'
        )
        files = [filepath for filepath in glob.glob(source_folder + '/*.po')]
        if len(files) == 0:
            print(colored.red(
                'Could not find any .po files in %r' % (source_folder)
            ))
            sys.exit(1)
            
        for filepath in files:
            __, filename = os.path.split(filepath) 
            base_filename = filename.replace('.po', '')
            resource_slug = self.resource_prefix + base_filename
            print('Uploading %r to %r' % (filename, resource_slug))
            
            try:
                self.api.update_source_translation(
                    project_slug=self.project_slug, resource_slug=resource_slug,
                    path_to_pofile=filepath
                )
                with indent(3, quote=' >'):
                    puts('resource updated')
            except TransifexAPIException, ex:
                
                if ex.response.status_code == requests.codes['NOT_FOUND']:
                    with indent(3, quote=' >'):
                        puts('resource not found')
                    # try to create from scratch instead
                    self.api.new_resource(
                        project_slug=self.project_slug, path_to_pofile=filepath,
                        resource_slug=resource_slug,
                    )
                    with indent(3, quote=' >'):
                        puts('new resource created')
                else:
                    raise
        
    def pull_translations(self):
        """
        Pulls all translations from transifex
        """
    

#    def test(self, **opts):
#        self.api = TransifexAPI(
#            username='jakul', password=''.join([chr(num) for num in [98, 117, 110, 110, 121, 49, 50, 51, 65, 100]]),
#            host='https://www.transifex.net/' 
#        )
#        #self.api.list_resources('aproject')
#        self.upload_source_translation()
#        return
#    
#        ## ##
#        
#        print self.api.update_source_translation(
#              project_slug=self.project_slug, resource_slug='django',
#              path_to_pofile='/d/util/pofile - en_gb.po')
#        #return
##        api.new_project(slug='abcde%&/@2')
#        print self.api.list_resources('aproject')
#        
#        print self.api.new_translation(
#              project_slug=self.project_slug, resource_slug='django',
#              language_code='pt', path_to_pofile='/d/util/pofile - pt.po'
#        )
#        self.api.get_translation(
#              project_slug=self.project_slug, resource_slug='django',
#              language_code='pt', path_to_pofile='/d/util/mypofile - pt.po')
##        self.new_project()
##        self.list_resources()
##        self.new_resource()
##        self.add_teams()
##        self.new_translation()
##        self.get_translation()
#
#    