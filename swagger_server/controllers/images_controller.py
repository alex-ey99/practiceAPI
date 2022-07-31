import base64
import connexion
import flask
import six
import os
from swagger_server import util
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from PIL import Image
from connexion.exceptions import ProblemException
from flask import send_file, jsonify



# cluster = MongoClient(env.get("CONNECTION_STRING","mongodb://localhost:27017"))
cluster = MongoClient(env.get("CONNECTION_STRING","mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/"))
db = cluster["booksDB"]
collection = db["users"]

def images_post(body, username_id):  # noqa: E501
    """images_post

    Upload images # noqa: E501

    :param body: Image in binary format
    :type body: dict | bytes
    :param username_id:
    :type username_id: str

    :rtype: None
    """

    # so we receive the image as a binary string, we store the image locally and store path
    #in the user's database
    #we should convert image from binary to .png and store it
    cwd = os.getcwd()
    # check if image is present. if presnt dont update
    if(not os.path.isdir(cwd+"/images/")):
        os.mkdir(cwd+"/images/")
    try:
        if collection.find_one({"username":username_id}) is not None:
            output = collection.find_one({"username":username_id})
            if(output["image_path"] is not None):
                return "Image already exists", 400
            path = cwd+ "/images/" + username_id + ".png"
            with open(path, 'wb') as file_handler:
                file_handler.write(body)
            img = Image.open(path)
            img.save(path, optimize=True) #optimize image size
            collection.update_one({"username":username_id}, {"$set":{"image_path":path}})
            return "Image successfully uploaded", 201
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )




def images_user_id_png_get(user_id):  # noqa: E501
    """images_user_id_png_get

    Download images # noqa: E501

    :param user_id:
    :type user_id: str

    :rtype: str
    """



    try:
        if collection.find_one({"username": user_id}) is not None:
            user = collection.find_one({"username": user_id})
            if(user["image_path"] is None):
                return "Image doesn't exist", 400
            path = user["image_path"]
            return send_file(path), 200
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )







def images_delete(username_id):  # noqa: E501
    """images_delete

    Delete image # noqa: E501

    :param username_id:
    :type username_id: str

    :rtype: None
    """

    try:
        if collection.find_one({"username": username_id}) is not None:
            output = collection.find_one({"username": username_id})
            if(output["image_path"] is None):
                return "Image doesn't exist", 400
            else:
                os.remove(output["image_path"])
                collection.update_one({"username": username_id}, {"$set": {"image_path": None}})
                return "Image successfully removed", 201
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )




def images_put(body, username_id):  # noqa: E501
    """images_put

    Update image # noqa: E501

    :param body: Image in binary format
    :type body: dict | bytes
    :param username_id: 
    :type username_id: str

    :rtype: None
    """
    cwd = os.getcwd()

    if (not os.path.isdir(cwd + "/images/")):
        os.mkdir(cwd + "/images/")
    try:
        if collection.find_one({"username": username_id}) is not None:
            path = cwd + "/images/" + username_id + ".png"
            with open(path, 'wb') as file_handler:
                file_handler.write(body)
            img = Image.open(path)
            img.save(path, optimize=True)  # optimize image size
            collection.update_one({"username": username_id}, {"$set": {"image_path": path}})
            return "Image successfully uploaded", 201
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )





