# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
import re  # noqa: F401,E501
from swagger_server import util


class User(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: str=None, username: str=None, password: str=None, role: str=None, token: str=None, image_path: str=None):  # noqa: E501
        """User - a model defined in Swagger

        :param id: The id of this User.  # noqa: E501
        :type id: str
        :param username: The username of this User.  # noqa: E501
        :type username: str
        :param password: The password of this User.  # noqa: E501
        :type password: str
        :param role: The role of this User.  # noqa: E501
        :type role: str
        :param token: The token of this User.  # noqa: E501
        :type token: str
        :param image_path: The image_path of this User.  # noqa: E501
        :type image_path: str
        """
        self.swagger_types = {
            'id': str,
            'username': str,
            'password': str,
            'role': str,
            'token': str,
            'image_path': str
        }

        self.attribute_map = {
            'id': '_id',
            'username': 'username',
            'password': 'password',
            'role': 'role',
            'token': 'token',
            'image_path': 'image_path'
        }
        self._id = id
        self._username = username
        self._password = password
        self._role = role
        self._token = token
        self._image_path = image_path

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this User.


        :return: The id of this User.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this User.


        :param id: The id of this User.
        :type id: str
        """

        self._id = id

    @property
    def username(self) -> str:
        """Gets the username of this User.


        :return: The username of this User.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this User.


        :param username: The username of this User.
        :type username: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this User.


        :return: The password of this User.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this User.


        :param password: The password of this User.
        :type password: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password

    @property
    def role(self) -> str:
        """Gets the role of this User.


        :return: The role of this User.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role: str):
        """Sets the role of this User.


        :param role: The role of this User.
        :type role: str
        """
        allowed_values = ["admin", "librarian", "student"]  # noqa: E501
        if role not in allowed_values:
            raise ValueError(
                "Invalid value for `role` ({0}), must be one of {1}"
                .format(role, allowed_values)
            )

        self._role = role

    @property
    def token(self) -> str:
        """Gets the token of this User.


        :return: The token of this User.
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token: str):
        """Sets the token of this User.


        :param token: The token of this User.
        :type token: str
        """

        self._token = token

    @property
    def image_path(self) -> str:
        """Gets the image_path of this User.


        :return: The image_path of this User.
        :rtype: str
        """
        return self._image_path

    @image_path.setter
    def image_path(self, image_path: str):
        """Sets the image_path of this User.


        :param image_path: The image_path of this User.
        :type image_path: str
        """

        self._image_path = image_path
