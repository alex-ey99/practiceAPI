# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_login_body import UserLoginBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_login_post(self):
        """Test case for user_login_post

        
        """
        body = UserLoginBody()
        response = self.client.open(
            '//user/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_logout_get(self):
        """Test case for user_logout_get

        
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '//user/logout',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_register_post(self):
        """Test case for user_register_post

        
        """
        body = User()
        response = self.client.open(
            '//user/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
