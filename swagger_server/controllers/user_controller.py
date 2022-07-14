import connexion
import six
import jwt
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_login_body import UserLoginBody  # noqa: E501
from swagger_server import util
import pymongo
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
from connexion.exceptions import ProblemException
from dotenv import load_dotenv, find_dotenv
from os import environ as env
import secrets

cluster = MongoClient("mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/")
db = cluster["booksDB"]
collection = db["users"]
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
SECRET = env.get("SECRET")
API_KEY = env.get("API_KEY")

def user_login_post(body):  # noqa: E501
    """user_login_post

    Login using username and password # noqa: E501

    :param body: Username, password
    :type body: dict | bytes

    :rtype: str
    """
    #we need to check if username is in the database and we need to generate a jwt token and return it
    #our jwt token will contain in the payload the username and a randomly generated token
    #this is a randomly generated token
    token = secrets.token_urlsafe(16);

    if connexion.request.is_json:
        body = UserLoginBody.from_dict(connexion.request.get_json())  # noqa: E501
        body.to_dict()
    uname = body.to_dict()["username"]
    pword = body.to_dict()["password"]

    try:
        query_output = collection.find_one({"username": uname})
        if query_output["password"] == pword:
            encoded = jwt.encode({"username": uname, "token": token }, SECRET , algorithm="HS256")
            collection.update_one({"username":uname},{"$set": {"token":token}})
            return encoded

        return"Invalid username or password", 400
    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def user_register_post(body):  # noqa: E501
    """user_register_post

    Register, by creating username and password # noqa: E501

    :param body: Username, password, role
    :type body: dict | bytes

    :rtype: None
    """
    # we need to register a user
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
        body.to_dict()
        username= body.to_dict()["username"]
    try:

        if collection.find_one({"username":username}) is None:
            query_output = collection.insert_one(body.to_dict())
            if query_output.inserted_id:
                return "User successfully registered", 201
            else:
                return 'Bad request', 400
        else:
            return "Username already exists", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def user_logout_get(username=None):  # noqa: E501
    """user_logout_get

     # noqa: E501

    :param username: Username to logout
    :type username: str

    :rtype: None
    """
    if(username):
        try:
            collection.update_one({"username": username},{"$set":{"token" : ""}})
            return "Successfully logged out user", 200
        except:
            raise ProblemException(
                status = 500,
                detail = "Error logging out user",
                title = "Internal server error"
            )

