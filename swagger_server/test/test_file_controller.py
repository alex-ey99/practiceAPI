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
                        ('title', 'title_example')]
        response = self.client.open(
            '//file',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_post(self):
        """Test case for file_post

        
        """
        data = dict(username='username_example',
                    title='title_example',
                    description='description_example',
                    file='file_example')
        response = self.client.open(
            '//file',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_put(self):
        """Test case for file_put

        
        """
        data = dict(file='file_example',
                    username='username_example',
                    old_title='old_title_example',
                    new_title='new_title_example',
                    new_description='new_description_example')
        response = self.client.open(
            '//file',
            method='PUT',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_file_username_title_get(self):
        """Test case for file_username_title_get

        
        """
        response = self.client.open(
            '//file/{username}/{title}'.format(username='username_example', title='title_example'),
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
