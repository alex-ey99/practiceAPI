import base64
import connexion
import flask
import six
import os
from swagger_server import util
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from connexion.exceptions import ProblemException
from flask import send_file, jsonify, send_from_directory
from swagger_server.models.file_ import File_

# cluster = MongoClient(env.get("CONNECTION_STRING","mongodb://localhost:27017"))
cluster = MongoClient(env.get("CONNECTION_STRING","mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/"))
db = cluster["booksDB"]
collection = db["users"]

acceptedFileTypes = {"text/plain":".txt","application/msword":".doc", "application/vnd.openxmlformats-officedocument.wordprocessingml.document":".docx","image/jpeg":".jpg","image/png":".png","application/pdf":".pdf"}

def file_post(username=None, title=None, description=None, file=None):  # noqa: E501
    """file_post

    Upload any file # noqa: E501

    :param username:
    :type username: str
    :param title:
    :type title: str
    :param description:
    :type description: str
    :param file:
    :type file: strstr

    :rtype: None
    """

    cwd = os.getcwd()
    if (not os.path.isdir(cwd + "/files/")):
        os.mkdir(cwd + "/files/")

    username = connexion.request.form["username"]
    title = connexion.request.form["title"]
    description = connexion.request.form["description"]
    file = connexion.request.files["file"]

    newFile = {
        "title" : title,
        "description" : description,
        "path" : ""
    }

    try:
        if collection.find_one({"username": username}) is not None:
            if file.mimetype in acceptedFileTypes:
                if (not os.path.isdir(cwd + "/files/" + username)):
                    os.mkdir(cwd + "/files/" + username)
                path = cwd + "/files/" + username +"/"+ title + acceptedFileTypes[file.mimetype]
                newFile["path"] = path
                if collection.find_one({"$and": [{"username": username}, {"files": {"$elemMatch": {"title": title}}}]}) is None:
                    file.save(path)
                    collection.update_one({"username": username}, {"$push": {"files": newFile}})
                    response = {"message": "File successfully uploaded"}
                    return jsonify(response), 201
                else:
                    response = {"message": "Title not unique"}
                    return jsonify(response), 400
            else:
                response = {"message": "Filetype is not accepted"}
                return jsonify(response), 400
        else:
            response = {"message": "Username doesn't exist"}
            return jsonify(response), 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )




def file_delete(username, title):  # noqa: E501
    """file_delete

    Delete file # noqa: E501

    :param username:
    :type username: str
    :param title:
    :type title: str

    :rtype: None
    """
    try:
        if collection.find_one({"username": username}) is not None:
            if collection.find_one(
                    {"$and": [{"username": username}, {"files": {"$elemMatch": {"title": title}}}]}) is not None:
                output = (collection.find_one({"username": username}))["files"]
                path = ""
                for file in output:
                    if file["title"] == title:
                        path = file["path"]
                os.remove(path)
                collection.update_one({"username": username}, {"$pull": {"files": {"title": title}}})
                response = {"message": "File successfully deleted"}
                return jsonify(response), 201
            else:
                response = {"message": "Title not found"}
                return jsonify(response), 400
        else:
            response = {"message": "Username doesn't exist"}
            return jsonify(response), 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


def file_put(file = None, username=None, old_title=None, new_title=None, new_description=None):  # noqa: E501
    """file_put

    Update file # noqa: E501

    :param file:
    :type file: strstr
    :param username:
    :type username: str
    :param old_title:
    :type old_title: str
    :param new_title:
    :type new_title: str
    :param new_description:
    :type new_description: str

    :rtype: None
    """
    cwd = os.getcwd()
    if (not os.path.isdir(cwd + "/files/")):
        os.mkdir(cwd + "/files/")

    username = connexion.request.form["username"]
    new_title = connexion.request.form["new_title"]
    old_title = connexion.request.form["old_title"]
    new_description = connexion.request.form["new_description"]
    file = connexion.request.files["file"]

    newFile = {
        "title": new_title,
        "description": new_description,
        "path": ""
    }

    try:
        if collection.find_one({"username": username}) is not None:
            if file.mimetype in acceptedFileTypes:
                if (not os.path.isdir(cwd + "/files/" + username)):
                    os.mkdir(cwd + "/files/" + username)
                newPath = cwd + "/files/" + username + "/" + new_title + acceptedFileTypes[file.mimetype]
                newFile["path"] = newPath
                if collection.find_one(
                        {"$and": [{"username": username}, {"files": {"$elemMatch": {"title": old_title}}}]}) is not None:
                    if collection.find_one(
                            {"$and": [{"username": username},
                                      {"files": {"$elemMatch": {"title": new_title}}}]}) is None:
                        output = (collection.find_one({"username": username}))["files"]
                        oldPath = ""
                        for f in output:
                            if f["title"] == old_title:
                                oldPath = f["path"]

                        file.save(newPath)
                        os.remove(oldPath)
                        collection.update_one({"username":username}, {"$pull":{"files": {"title": old_title}}})
                        collection.update_one({"username": username}, {"$push": {"files": newFile}})
                        response = {"message": "File successfully uploaded"}

                        return jsonify(response), 201
                    else:
                        response = {"message": "New title is not unique"}
                        return jsonify(response), 400

                else:
                    response = {"message": "Title not found"}
                    return jsonify(response), 400
            else:
                response = {"message": "Filetype is not accepted"}
                return jsonify(response), 400
        else:
            response = {"message": "Username doesn't exist"}
            return jsonify(response), 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )



def file_username_title_get(username, title):  # noqa: E501
    """file_username_title_get

    Download file # noqa: E501

    :param username:
    :type username: str
    :param title:
    :type title: str

    :rtype: str
    """
    try:
        if collection.find_one({"username": username}) is not None:
            if collection.find_one(
                    {"$and": [{"username": username}, {"files": {"$elemMatch": {"title": title}}}]}) is not None:
                output = (collection.find_one({"username": username}))["files"]

                for file in output:
                    if file["title"] == title:
                        # if(extension == "png" or extension == "txt" or extension=="jpg"):
                        #     return send_file(file), 200
                        # else:
                        return send_file(file["path"], mimetype= "application/octet-stream",  as_attachment=True), 200
            else:
                response = {"message":"Title doesn't exist"}
                return jsonify(response), 400

        else:
            response = {"message":"Username doesn't exist"}
            return jsonify(response), 400

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
            output = (collection.find_one({"username": username}))["files"]
            if output is not None:
                path = ""
                for file in output:
                        path = file["path"]
                        os.remove(path)
                        collection.update_one({"username": username}, {"$pull": {"files": {"path": path}}})
                response = {"message": "Files successfully deleted"}
                return jsonify(response), 201
            else:
                response = {"message":"No files to delete"}
                return jsonify(response), 400
        else:
            response = {"message": "Username doesn't exist"}
            return jsonify(response), 400

    except:
        raise ProblemException(
            status=500,
            detail="Internal server error",
            title="Server error"
        )


