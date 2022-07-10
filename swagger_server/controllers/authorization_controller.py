from typing import List
import jwt
from flask import request
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from connexion import ProblemException
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
SECRET = env.get("SECRET")
API_KEY = env.get("API_KEY")

# encoded = jwt.encode({"some":"payload"}, SECRET, algorithm ="HS256")

# decoded = jwt.decode(encoded, SECRET, algorithms="HS256")


def check_auth(api_key, required_scopes):
    #The api_key received is an encoded JWT, the payload has the api_key
    #.env stores the SECRET used to encode and decode the JWT
    #.env also stores the api_key
    api_key_decoded = jwt.decode(api_key, SECRET,algorithms="HS256" )
    if api_key_decoded["api_key"] == API_KEY:
        return {'test_key':'test_value'}
    else:
        raise ProblemException(
            status=401,
            detail="Unauthorized access",
            title="Incorrect api_key"
        )


