# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_image_delete(self):
        """Test case for image_delete

        
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '//image',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_post(self):
        """Test case for image_post

        
        """
        body = Object()
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '//image',
            method='POST',
            data=json.dumps(body),
            content_type='image/png',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_put(self):
        """Test case for image_put

        
        """
        body = Object()
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '//image',
            method='PUT',
            data=json.dumps(body),
            content_type='image/png',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_username_png_get(self):
        """Test case for image_username_png_get

        
        """
        response = self.client.open(
            '//image/{username}.png'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
