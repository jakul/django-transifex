from unittest import TestCase
from mock import patch, MagicMock, Mock
from djangotransifex.api import DjangoTransifexAPI
from django.utils.unittest.case import skip
from djangotransifex.exceptions import DjangoTransifexAPIException
import json

class DjangoTransifexAPITest(TestCase):
    
    def setUp(self):
        data = {
            'username': 'aaa', 'password': 'aaa',
            'host': 'http://www.mydomain.com'
        }
        self.api = DjangoTransifexAPI(**data)
        
    @patch('__builtin__.open', create=True)
    @patch('glob.glob')
    @patch('requests.put')
    def test_upload_source_translations(self, mock_requests_put, mock_glob, 
                                        mock_open):
        """
        Ensure that `upload_source_translations` works 
        """
        mock_glob.return_value = [
            '/a/b/c/locale/en-gb/LC_MESSAGES/django.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/djangojs.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/another.po',
        ]
        file_contents = 'aaaaaa\nggggg'
        mock_open.return_value = MagicMock(spec=file)
        mock_open.return_value.read = lambda: file_contents
        
        def side_effect(*args, **kwargs):
            response = Mock()
            response.status_code = 200
            response.content = json.dumps({'a': 1})
            return response
        mock_requests_put.side_effect = side_effect
        
        self.api.upload_source_translations(project_slug='aaa')
        
        self.assertEqual(mock_requests_put.call_count, 3)
        
    @patch('glob.glob')
    def test_upload_source_translations_no_files_found(self, mock_glob):
        """
        Ensure that `upload_source_translations` works when there are no 
        localisation files in the source language
        """
        mock_glob.return_value = []
        self.assertRaises(
            DjangoTransifexAPIException, self.api.upload_source_translations,
            project_slug='aaa'
        )
        
        
    @skip('Not implemented yet')
    @patch('requests.post')
    def test_upload_source_translations_no_project(self, mock_requests):
        """
        Ensure that `upload_source_translations` works when there project
        has not been created
        """
        
    @patch('__builtin__.open', create=True)
    @patch('glob.glob')
    @patch('requests.put')
    @patch('requests.post')
    def test_upload_source_translations_no_resources(self, mock_requests_post,
                                                     mock_requests_put,
                                                     mock_glob, mock_open):
        """
        Ensure that `upload_source_translations` works when the resources
        being uploaded haven't been created
        """
        mock_glob.return_value = [
            '/a/b/c/locale/en-gb/LC_MESSAGES/django.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/djangojs.po',
            '/a/b/c/locale/en-gb/LC_MESSAGES/another.po',
        ]
        file_contents = 'aaaaaa\nggggg'
        mock_open.return_value = MagicMock(spec=file)
        mock_open.return_value.read = lambda: file_contents
        
        def mock_requests_put_side_effect(*args, **kwargs):
            response = Mock()
            response.status_code = 404
            return response
        mock_requests_put.side_effect = mock_requests_put_side_effect
        
        def mock_requests_post_side_effect(*args, **kwargs):
            response = Mock()
            response.status_code = 201
            return response
        mock_requests_post.side_effect = mock_requests_post_side_effect
        
        
        self.api.upload_source_translations(project_slug='aaa')
        
        self.assertEqual(mock_requests_post.call_count, 3)
    