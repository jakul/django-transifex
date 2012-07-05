from transifex.api import TransifexAPI
import os
import app_settings
import glob
from transifex.exceptions import TransifexAPIException
import requests
from djangotransifex.exceptions import LanguageCodeNotAllowed, NoPoFilesFound, \
    ProjectNotFound, ResourceNotFound
from django.conf import settings

class DjangoTransifexAPI(TransifexAPI):
    
    def upload_source_translations(self, project_slug):
        """
        Uploads the current translations as a new source translations. 
        
        This command will create resources if they don't already exist in the
        project
        
        @param project_slug
            the project slug
            
        @return 
        """


        source_folder = os.path.join(
             app_settings.PROJECT_PATH, 'locale',
             app_settings.SOURCE_LANGUAGE_CODE, 'LC_MESSAGES'
        )
        files = [filepath for filepath in glob.glob(source_folder + '/*.po')]
        if len(files) == 0:
            # No source files
            raise NoPoFilesFound(
                'Could not find any .po files in %r' % (source_folder)
            )
            
        # First check that the project exists on transifex
        if not self.project_exists(project_slug):
            self.new_project(slug=project_slug)

        # Second: upload the individual source .po files to resources in that
        # project
        for filepath in files:
            __, filename = os.path.split(filepath) 
            base_filename = filename.replace('.po', '')
            resource_slug = app_settings.RESOURCE_PREFIX + base_filename
            
            try:
                self.update_source_translation(
                    project_slug=project_slug, resource_slug=resource_slug,
                    path_to_pofile=filepath
                )
            except TransifexAPIException, ex:
                if hasattr(ex, 'response') and ex.response.status_code == \
                requests.codes['NOT_FOUND']:
                    # Resource doesn't exist                        
                    # Create a new resource from scratch instead
                    self.new_resource(
                        project_slug=project_slug, path_to_pofile=filepath,
                        resource_slug=resource_slug,
                    )
                else:
                    # Unknown exception
                    raise
                
    def upload_translations(self, project_slug, language_code):
        """
        Uploads the current translations for the given language to Transifex. 
        
        This command will overwrite translations made on the Transifex server 
        

        @param project_slug
            The project slug
        @param language_code
            The language code to upload. This should be the language code used
            in the Django project, not the code used on Transifex.
            
        @return 
            None
            
        @raises LanguageCodeNotAllowed
            If the language code given is not listed in settings.LANGUAGES
        @raises NoPoFilesFound
            If there are no po files in the language folder for the given
            language
        @raises ProjectNotFound
            If the project does not exist on the Transifex server   
        @raises NoSourceLanguage
            If the translation being uploaded doesn't have a source language
            translation     
        """
        if language_code not in [code for code, __ in settings.LANGUAGES]:
            raise LanguageCodeNotAllowed(language_code)
        
        folder = os.path.join(
             app_settings.PROJECT_PATH, 'locale', language_code, 'LC_MESSAGES'
        )
        files = [filepath for filepath in glob.glob(folder + '/*.po')]
        if len(files) == 0:
            # No source files
            raise NoPoFilesFound(
                'Could not find any .po files in %r' % (folder)
            )
            
        # First check that the project exists on transifex
        if not self.project_exists(project_slug):
            raise ProjectNotFound(project_slug)

        # Second: upload the individual .po files to resources in that
        # project
        for filepath in files:
            __, filename = os.path.split(filepath) 
            base_filename = filename.replace('.po', '')
            resource_slug = app_settings.RESOURCE_PREFIX + base_filename
            
            try:
                # Transifex will automatically convert from our language codes
                # to theirs
                self.new_translation(
                    project_slug=project_slug, resource_slug=resource_slug,
                    path_to_pofile=filepath, language_code=language_code
                )
            except TransifexAPIException, ex:
                if hasattr(ex, 'response') and ex.response.status_code == \
                requests.codes['NOT_FOUND']:
                    # Resource doesn't exist
                    raise ResourceNotFound(resource_slug)
                else:
                    # Unknown exception
                    raise
                
    def pull_translations(self, project_slug, source_language):
        """
        Pull all translations from the remote Transifex server to the local
        machine, creating the folders where needed

        @param project_slug
            The project slug
        @param source_language
            The source language code.
            This should be the *Transifex* language code 
        
        @return None
        
        @raises ProjectNotFound
            If the project does not exist on the Transifex server    
        """
        # First check that the project exists on transifex
        if not self.project_exists(project_slug):
            raise ProjectNotFound(project_slug)

        resources = self.list_resources(project_slug)
        for resource in resources:
            resource_slug = resource['slug']
            languages = self.list_languages(project_slug, resource_slug)
            
            # remove the source language code
            languages = [
                language for language in languages
                if language != source_language
            ]
            
            for transifex_language_code in languages:
                local_language_code = self._convert_to_local_language_code(
                    transifex_language_code
                )
                pofile_dir = os.path.join(
                    app_settings.PROJECT_PATH, 'locale', local_language_code,
                    'LC_MESSAGES'
                )
                if not os.path.exists(pofile_dir):
                    os.makedirs(pofile_dir)
                path_to_pofile = os.path.join(pofile_dir, resource_slug + '.po')
                self.get_translation(
                    project_slug, resource_slug, transifex_language_code,
                    path_to_pofile
                )
                
    def _convert_to_local_language_code(self, transifex_language_code):
        """
        Converts a transifex language code to a local one
        """
        return app_settings.LANGUAGE_MAPPING.get(
            transifex_language_code, transifex_language_code
        )