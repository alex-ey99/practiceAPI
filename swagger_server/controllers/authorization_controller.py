from typing import List
import jwt
from flask import request
from pymongo import MongoClient
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

# cluster = MongoClient("mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/")
cluster = MongoClient(env.get("CONNECTION_STRING","mongodb://localhost:27017"))
db = cluster["booksDB"]
collection = db["users"]



def check_auth(jwtToken, required_scopes):
    #The api_key received is an encoded JWT, the payload has a token and username
    #the token sent back by the user contains the username
    # we will check if for that username the token is the same

    jwtDecoded = jwt.decode(jwtToken, SECRET,algorithms="HS256" )
    try:
        uname = jwtDecoded["username"]
        query_output = collection.find_one({"username":uname})

        if query_output["token"] == jwtDecoded["token"]:
            return {'username': uname}
        else:
            raise ProblemException(
                status=401,
                detail="Unauthorized access",
                title="Incorrect token"
            )


    except:
        raise ProblemException(
            status =401,
            detail=" Unauthorized access",
            title= "Incorrect token"
        )