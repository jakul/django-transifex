from unittest import TestCase
from mock import patch, MagicMock, Mock
from djangotransifex.api import DjangoTransifexAPI
from django.utils.unittest.case import skip
from djangotransifex.exceptions import NoPoFilesFound, LanguageCodeNotAllowed,\
    ProjectNotFound, ResourceNotFound
import json

class _BaseDjangoTransifexAPITest(TestCase):

    def setUp(self):
        data = {
            'username': 'aaa', 'password': 'aaa',
            'host': 'http://www.areallynonexistentdomaiihope.com'
        }
        self.api = DjangoTransifexAPI(**data)
        
    def _mock_response(self, status_code, content=None):
        response = Mock()
        response.status_code = status_code
        if content:
            response.content = json.dumps(content)
        return response
        
class DjangoTransifexAPITest(_BaseDjangoTransifexAPITest):
    
    def setUp(self):
        super(DjangoTransifexAPITest, self).setUp()
        
        self.patchers = {}
        self.patchers['mock_open'] = patch('__builtin__.open', create=True
        )
        self.patchers['mock_glob'] = patch('glob.glob')
        self.patchers['mock_requests_put'] = patch('requests.put')
        self.patchers['mock_requests_post'] = patch('requests.post')
        self.patchers['mock_project_exists'] = patch(
            'djangotransifex.api.DjangoTransifexAPI.project_exists'
        )
        self.patchers['mock_new_project'] = patch(
            'djangotransifex.api.DjangoTransifexAPI.new_project'                                                  
        )

        for name, patcher in self.patchers.items():
            setattr(self, name, patcher.start())
            
        self.mock_glob.return_value = [
            '/a/b/c/locale/en-gb/LC_MESSAGES/django.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/djangojs.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/another.po',
        ]
        file_contents = 'aaaaaa\nggggg'
        self.mock_open.return_value = MagicMock(spec=file)
        self.mock_open.return_value.read = lambda: file_contents   

    def tearDown(self):
        for patcher in self.patchers.values():
            patcher.stop()

    def test_upload_source_translations(self):
        """
        Ensure that `upload_source_translations` works 
        """
        self.mock_requests_put.side_effect = lambda *args,**kwargs: \
            self._mock_response(200, {'a':1})
        self.mock_project_exists.return_value = True        
        
        self.api.upload_source_translations(project_slug='aaa')
        
        self.assertEqual(self.mock_requests_put.call_count, 3)
        
    def test_upload_source_translations_no_files_found(self):
        """
        Ensure that `upload_source_translations` works when there are no 
        localisation files in the source language
        """
        self.mock_glob.return_value = []
        
        self.assertRaises(
            NoPoFilesFound, self.api.upload_source_translations,
            project_slug='aaa'
        )

    def test_upload_source_translations_no_project(self):
        """
        Ensure that `upload_source_translations` works when there project
        has not been created
        """        
        self.mock_requests_put.side_effect = lambda *args,**kwargs: \
            self._mock_response(200, {'a':1})
        self.mock_project_exists.return_value = False
        self.mock_new_project.return_value = None
        
        self.api.upload_source_translations(project_slug='aaa')
        
        self.assertEqual(self.mock_requests_put.call_count, 3)
        self.assertTrue(self.mock_new_project.called)

    def test_upload_source_translations_no_resources(self):
        """
        Ensure that `upload_source_translations` works when the resources
        being uploaded haven't been created
        """
        self.mock_requests_put.side_effect = lambda *args,**kwargs: \
            self._mock_response(404)        
        self.mock_requests_post.side_effect = lambda *args,**kwargs: \
            self._mock_response(201)
        self.mock_project_exists.return_value = True        
        
        self.api.upload_source_translations(project_slug='aaa')
        self.assertEqual(self.mock_requests_post.call_count, 3)
        
    @patch('djangotransifex.api.DjangoTransifexAPI.new_translation')
    def test_upload_translations(self, mock_new_translation):
        """
        Ensure that the `upload_translations` function works
        """
        self.mock_project_exists.return_value = True
        
        self.api.upload_translations(project_slug='aaa', language_code='it')
        
        self.assertTrue(mock_new_translation.called)
        
    
    def test_upload_translations_bad_language_code(self):
        """
        Ensure that the `upload_translations` function works when a bad language
        code is provided
        """
        self.assertRaises(
            LanguageCodeNotAllowed, self.api.upload_translations,
            project_slug='aaa', language_code='abc'
        )
    
    def test_upload_translations_no_po_files(self):
        """
        Ensure that the `upload_translations` function works when there are no
        source po files
        """
        self.mock_glob.return_value = []
        
        self.assertRaises(
            NoPoFilesFound, self.api.upload_translations,
            project_slug='aaa', language_code='it'
        )
    
    def test_upload_translations_project_not_found(self):
        """
        Ensure that the `upload_translations` function works when Transifex
        cannot find the project
        """
        self.mock_project_exists.return_value = False
        
        self.assertRaises(
            ProjectNotFound, self.api.upload_translations,
            project_slug='aaa', language_code='it'
        )
    
    def test_upload_translations_resource_not_found(self):
        """
        Ensure that the `upload_translations` function works when the resource
        is not found
        """
        self.mock_requests_put.side_effect = lambda *args,**kwargs: \
            self._mock_response(404)
        
        self.assertRaises(
            ResourceNotFound, self.api.upload_translations,
            project_slug='aaa', language_code='it'
        )


class DjangoTransifexAPIPullTranslationsTest(_BaseDjangoTransifexAPITest):
    """
    Test the `pull_translations` function of the Django Transifex API
    """
    
    def setUp(self):
        super(DjangoTransifexAPIPullTranslationsTest, self).setUp()
                
        #setup patches
        self.patchers = {}
        self.patchers['mock_list_resources'] = patch(
            'djangotransifex.api.DjangoTransifexAPI.list_resources'
        )
        self.patchers['mock_list_languages'] = patch(
          'djangotransifex.api.DjangoTransifexAPI.list_languages'
        )
        self.patchers['mock_exists'] = patch('os.path.exists')
        self.patchers['mock_makedirs'] = patch('os.makedirs')
        self.patchers['mock_get_translation'] = patch(
            'djangotransifex.api.DjangoTransifexAPI.get_translation'
        )
        self.patchers['mock_project_exists'] = patch(
            'djangotransifex.api.DjangoTransifexAPI.project_exists'
        )

        for name, patcher in self.patchers.items():
            setattr(self, name, patcher.start())
        
    def tearDown(self):
        for patcher in self.patchers.values():
            patcher.stop()
        
            
    def test_pull_translations(self):
        """
        Ensure that the `pull_translations` function works
        """
        self.mock_list_resources.return_value = [
            {'slug': 'abc'}, {'slug': 'def'}
        ]
        self.mock_list_languages.return_value = ['en_GB', 'it']
        self.mock_exists.return_value = True
        
        self.api.pull_translations(project_slug='abc', source_language='en-gb')
        
        self.assertEqual(self.mock_get_translation.call_count, 4)
    
    def test_pull_translations_no_project(self):
        """
        Ensure that the `pull_translations` function works when Transifex 
        cannot find the project
        """
        self.mock_project_exists.return_value = False
        
        self.assertRaises(
            ProjectNotFound, self.api.pull_translations,
            project_slug='aaa', source_language='it'
        )
    
    def test_pull_translations_no_folders(self):
        
        """
        Ensure that the `pull_translations` function works when there are no
        locale folders on the local machine
        """
        self.mock_project_exists.return_value = True
        self.mock_list_resources.return_value = [
            {'slug': 'abc'}, {'slug': 'def'}
        ]
        self.mock_list_languages.return_value = ['en_GB', 'it']
        self.mock_exists.return_value = False
        
        self.api.pull_translations(project_slug='abc', source_language='en-gb')
        
        self.assertEqual(self.mock_get_translation.call_count, 4)
        self.assertEqual(self.mock_makedirs.call_count, 4)
    
    def test_pull_translations_different_local_language_code(self):
        """
        Ensure that the `pull_translations` function works for a language which
        has a different local language code to transifex one
        """
        self.mock_project_exists.return_value = True
        self.mock_list_resources.return_value = [{'slug': 'abc'}]
        self.mock_list_languages.return_value = ['en_GB','it_IT']
        self.mock_exists.return_value = True
        
        self.api.pull_translations(project_slug='abc', source_language='en_GB')
        
        self.assertEqual(self.mock_get_translation.call_count, 1)
        saved_pofile_path = self.mock_get_translation.call_args[0][3] 
        self.assertTrue(saved_pofile_path.endswith('it/LC_MESSAGES/abc.po'))
    
    