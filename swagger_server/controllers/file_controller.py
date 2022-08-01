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

acceptedFileTypes = {"text/plain":".txt","application/msword":".doc", "application/vnd.openxmlformats-officedocument.wordprocessingml.document":".docx","image/jpeg":".jpg","image/png":".png","application/pdf":".pdf"}

def file_delete(username, extension):  # noqa: E501
    """file_delete

    Delete file # noqa: E501

    :param username:
    :type username: str
    :param extension:
    :type extension: str

    :rtype: None
    """

    try:
        if collection.find_one({"username": username}) is not None:
            output = collection.find_one({"username": username})
            files = output["files"]
            found = False
            for file in files:
                if (username+'.' +extension) in file:
                    found = True
                    os.remove(file)
                    collection.update_one({"username":username}, {"$pull":{"files":file}})
            if found:
                return "Successfully deleted file", 201
            else:
                return "Filetype doesn't exist", 400

        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def file_post(file, username):  # noqa: E501
    """file_post

    Upload any file # noqa: E501

    :param file:
    :type file: strstr
    :param username:
    :type username: str

    :rtype: None
    """

    #use mimetype to determine file type
    cwd = os.getcwd()
    if(not os.path.isdir(cwd+"/files/")):
        os.mkdir(cwd+"/files/")
    try:
        if collection.find_one({"username": username}) is not None:
            if file.mimetype in acceptedFileTypes:
                path = cwd+ "/files/" + username + acceptedFileTypes[file.mimetype]
                if collection.find_one({"$and":[{"username":username},{"files":path}]}) is None:
                    file.save(path)
                    collection.update_one({"username": username}, {"$push": {"files": path}})
                    return "File successfully uploaded", 201
                else:
                    return "Filetype already exists", 400
            else:
                return "Filetype is not accepted", 400
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )

def file_put(file, username):  # noqa: E501
    """file_put

    Update file # noqa: E501

    :param file:
    :type file: strstr
    :param username:
    :type username: str

    :rtype: None
    """

    cwd = os.getcwd()
    if (not os.path.isdir(cwd + "/files/")):
        os.mkdir(cwd + "/files/")
    try:
        if collection.find_one({"username": username}) is not None:
            if file.mimetype in acceptedFileTypes:
                path = cwd + "/files/" + username + acceptedFileTypes[file.mimetype]
                if collection.find_one({"$and": [{"username": username}, {"files": path}]}) is not None:
                    file.save(path)
                    return "File successfully uploaded", 201
                else:
                    return "No file to update", 400
            else:
                return "Filetype is not accepted", 400
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def file_username_extension_get(username, extension):  # noqa: E501
    """file_username_extension_get

    Download file # noqa: E501

    :param username:
    :type username: str
    :param extension:
    :type extension: str

    :rtype: str
    """
    try:
        if collection.find_one({"username": username}) is not None:
            output = collection.find_one({"username": username})
            files = output["files"]
            found = False
            for file in files:
                if (username + '.' + extension) in file:
                    found = True
                    if(extension == "png" or extension == "txt" or extension=="jpg"):
                        return send_file(file), 200
                    else:
                        return send_file(file, as_attachment=True, attachment_filename=username+'.'+extension), 200
            else:
                return "Filetype doesn't exist", 400

        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def files_delete(username):  # noqa: E501
    """files_delete

    Delete all files associated with a username # noqa: E501

    :param username:
    :type username: str

    :rtype: None
    """
    try:
        if collection.find_one({"username": username}) is not None:
            output = collection.find_one({"username": username})
            files = output["files"]
            found = False
            for file in files:
                found = True
                os.remove(file)
                collection.update_one({"username": username}, {"$pull": {"files": file}})
            if found:
                return "Successfully deleted files", 201
            else:
                return "No files under this username", 400
        else:
            return "Username doesn't exist", 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )












