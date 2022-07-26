# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestImagesController(BaseTestCase):
    """ImagesController integration test stubs"""

    def test_images_delete(self):
        """Test case for images_delete

        
        """
        query_string = [('username_id', 'username_id_example')]
        response = self.client.open(
            '//images',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_post(self):
        """Test case for images_post

        
        """
        body = Object()
        query_string = [('username_id', 'username_id_example')]
        response = self.client.open(
            '//images',
            method='POST',
            data=json.dumps(body),
            content_type='image/png',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_put(self):
        """Test case for images_put

        
        """
        body = Object()
        query_string = [('username_id', 'username_id_example')]
        response = self.client.open(
            '//images',
            method='PUT',
            data=json.dumps(body),
            content_type='image/png',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_images_user_id_png_get(self):
        """Test case for images_user_id_png_get

        
        """
        response = self.client.open(
            '//images/{user_id}.png'.format(user_id='user_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
