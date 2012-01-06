from transifex.api import TransifexAPI
import os
import app_settings
import glob
from clint.textui.core import indent, puts
from transifex.exceptions import TransifexAPIException
import requests
from djangotransifex.exceptions import DjangoTransifexAPIException

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
        # TODO: Check project exists
        # TODO: Add verbosity to extract CLI output
        
        source_folder = os.path.join(
             app_settings.PROJECT_PATH, 'locale',
             app_settings.SOURCE_LANGUAGE_CODE, 'LC_MESSAGES'
        )
        files = [filepath for filepath in glob.glob(source_folder + '/*.po')]
        if len(files) == 0:
            # No source files
            raise DjangoTransifexAPIException(
                'Could not find any .po files in %r' % (source_folder)
            )
            
#        # First check that the project exists on transifex
#        if not self.api.project_exists(project_slug):
#            raise DjangoTransifexAPIException(
#                'Project %r does not exist at %r' % (
#                    project_slug, self.host
#                )
#            ))
        
        # Second: upload the individual source .po files to resources in that
        # project
        for filepath in files:
            __, filename = os.path.split(filepath) 
            base_filename = filename.replace('.po', '')
            resource_slug = app_settings.RESOURCE_PREFIX + base_filename
            print('Uploading %r to %r' % (filename, resource_slug))
            
            try:
                self.update_source_translation(
                    project_slug=project_slug, resource_slug=resource_slug,
                    path_to_pofile=filepath
                )
                with indent(3, quote=' >'):
                    puts('resource updated')
            except TransifexAPIException, ex:
                if hasattr(ex, 'response') and ex.response.status_code == \
                requests.codes['NOT_FOUND']:
                    # Resource doesn't exist
                    with indent(3, quote=' >'):
                        puts('Resource not found')
                        
                    # Create a new resource from scratch instead
                    self.new_resource(
                        project_slug=project_slug, path_to_pofile=filepath,
                        resource_slug=resource_slug,
                    )
                    with indent(3, quote=' >'):
                        puts('New resource created')
                else:
                    # Unknown exception
                    raise