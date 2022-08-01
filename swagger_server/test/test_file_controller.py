# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    def test_file_delete(self):
        """Test case for file_delete

        
        """
        query_string = [('username', 'username_example'),
                        ('extension', 'extension_example')]
        response = self.client.open(
            '//file',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_post(self):
        """Test case for file_post

        
        """
        query_string = [('username', 'username_example')]
        data = dict(file='file_example')
        response = self.client.open(
            '//file',
            method='POST',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_put(self):
        """Test case for file_put

        
        """
        query_string = [('username', 'username_example')]
        data = dict(file='file_example')
        response = self.client.open(
            '//file',
            method='PUT',
            data=data,
            content_type='multipart/form-data',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_username_extension_get(self):
        """Test case for file_username_extension_get

        
        """
        response = self.client.open(
            '//file/{username}.{extension}'.format(username='username_example', extension='extension_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_files_delete(self):
        """Test case for files_delete

        
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '//files',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
