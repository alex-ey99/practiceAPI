import connexion
import six
import pymongo
from flask import Flask, jsonify
from pymongo import MongoClient
from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util
from bson import ObjectId
from os import environ as env
from dotenv import load_dotenv, find_dotenv

from connexion.exceptions import ProblemException


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# cluster = MongoClient("mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/")
# cluster = MongoClient(env.get("CONNECTION_STRING","mongodb://localhost:27017"))
cluster = MongoClient(env.get("CONNECTION_STRING","mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/"))
db = cluster["booksDB"]
collection = db["books"]
collectionUsers = db["users"]



def books_get():  # noqa: E501
    """books_get

    Return all the books available in the library # noqa: E501


    :rtype: List[Book]
    """

    try:
        results = collection.find({})

        books = []
        for result in results:
            books.append(Book.from_dict(result))
            print(result)
         # print(books)
        return books, 200
    except:
        raise ProblemException(
            status=500,
            detail="Error getting books",
            title="Internal Server Error"
        )




def books_id_delete(_id):  # noqa: E501
    """books_id_delete

    Delete the book with the specified ID # noqa: E501

    :param id: ID of the book to delete
    :type id: str

    :rtype: None
    """


    username= connexion.context["token_info"]
    role = collectionUsers.find_one(username)["role"]
    if(role=="admin" or role=="librarian"):
        try:
            query_output = collection.delete_one({"_id": ObjectId(_id)})
            if(query_output.deleted_count==1):
                return "Book successfully removed", 201
            else:
                return "Book with the requested ID not found", 404
        except:
            raise ProblemException(
                status=500,
                detail="Error deleting book",
                title="Internal Server Error"
            )
    else:
        raise ProblemException(
            status=401,
            detail ="Only admins and librarians can delete books",
            title= "Unauthorized access"
        )





def books_id_get(_id):  # noqa: E501
    """books_id_get

    Return the details about the book with the requested ID # noqa: E501

    :param id: ID of the book to request
    :type id: str

    :rtype: Book
    """


    try:
        if collection.find_one({"_id" : ObjectId(_id)}) is None:
            return "Book with the requested ID not found", 404
        else:
            result = collection.find_one({"_id" : ObjectId(_id)})
            result["_id"] = str(result.get("_id"))
            returned_book = Book.from_dict(result)
            return returned_book, 200
    except:
        raise ProblemException(
            status=500,
            detail="Error getting book with specified id",
            title="Internal server error"
        )



def books_id_put(body, _id):  # noqa: E501
    """books_id_put

    Update the details about the book with the specified ID # noqa: E501

    :param body: New details of the book to be modified
    :type body: dict | bytes
    :param id: ID of the book to modify
    :type id: str

    :rtype: None
    """
    username = connexion.context["token_info"]
    role = collectionUsers.find_one(username)["role"]
    if (role == "admin" or role == "librarian"):
        try:

            query_output = collection.update_one({"_id": ObjectId(_id)},{"$set":connexion.request.get_json()})
            if query_output.modified_count==1:
                return "Book successfully updated", 200
            else:
                return "Book with the requested ID not found", 404

        except:
            raise ProblemException(
                status=500,
                detail="Error updating book with specified id",
                title="Internal server error"
            )
    else:
        raise ProblemException(
            status=401,
            detail ="Only admins and librarians can delete books",
            title= "Unauthorized access"
        )



def books_post(body):  # noqa: E501
    """books_post

    Add a new book to the library # noqa: E501

    :param body: Details of the book to add
    :type body: dict | bytes

    :rtype: None
    """

    try:

        if connexion.request.is_json:
            body = Book.from_dict(connexion.request.get_json()) # noqa: E501
            body.to_dict()

        query_output = collection.insert_one(body.to_dict())

        if query_output.inserted_id:
            # return {
            #     "inserted_id": str(query_output.inserted_id)
            # }, 201
            return "Book successfully added to the library", 201
        else:
            return "Bad request", 400
    except:
        raise ProblemException(
            status=500,
            detail="Error adding book to the library",
            title="Internal server error"
        )






def books_search_get(title=None, year=None, author=None, genre=None):  # noqa: E501
    """books_search_get

    Get all the books matching your search criteria # noqa: E501

    :param title: Book title
    :type title: str
    :param year: Publication year
    :type year: int
    :param author: Book author
    :type author: str
    :param genre: Type of book
    :type genre: str

    :rtype: List[Book]
    """
    book = {}
    if(title): book["title"] = title
    if(year): book["year"] = year
    if(author): book["author"] = author
    if(genre): book["genre"] = genre
    try:

        results = collection.find(book)
        books = []
        for result in results:
            books.append(Book.from_dict(result))

        # print(books)
        if len(books) ==0:
            return "No book with such criteria found", 404
        else:
            return books, 200
    except:
        raise ProblemException(
            status=500,
            detail="Error finding book with such criteria",
            title="Internal server error"
        )




