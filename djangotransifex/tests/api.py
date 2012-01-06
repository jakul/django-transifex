from unittest import TestCase
from transifex.api import TransifexAPI
from mock import patch, Mock, MagicMock
from djangotransifex.api import DjangoTransifexAPI
from django.utils.unittest.case import skip

class DjangoTransifexAPITest(TestCase):
    
    def setUp(self):
        data = {
            'username': 'aaa', 'password': 'aaa',
            'host': 'http://www.mydomain.com'
        }
        self.api = DjangoTransifexAPI(**data)
        
    @patch('requests.post')
    def test_upload_source_translations(self, mock_requests):
        """
        Ensure that `upload_source_translations` works 
        """
        
    @patch('glob.glob')
    def test_upload_source_translations_no_files_found(self, mock_glob):
        """
        Ensure that `upload_source_translations` works when there are no 
        localisation files in the source language
        """
        mock_glob.return_value = []
        
        self.api.upload_source_translations(project_slug='aaa')
        
        
    @skip('Not implemented yet')
    @patch('requests.post')
    def test_upload_source_translations_no_project(self, mock_requests):
        """
        Ensure that `upload_source_translations` works when there project
        has not been created
        """
        
    @patch('requests.post')
    def test_upload_source_translations_no_resources(self, mock_requests):
        """
        Ensure that `upload_source_translations` works when the resources
        being uploaded haven't been created
        """
#        """
#        Test creating a new project with only the required arguments
#        """
#
#        def side_effect(*args, **kwargs):
#            response = Mock()
#            data = json.loads(kwargs.get('data', "{}"))
#            if 'source_language_code' in data and 'name' in data and 'slug' in \
#            data:
#                response.status_code = 201
#            else:
#                response.status_code = 400
#                
#            return response
#        
#        mock_requests.side_effect = side_effect 
#        self.api.new_project(slug='abc')
    