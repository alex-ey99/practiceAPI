import connexion
import six
import pymongo
from flask import Flask, jsonify
from pymongo import MongoClient
from swagger_server.models.book import Book  # noqa: E501
from swagger_server import util
from bson import ObjectId

from connexion.exceptions import ProblemException
cluster = MongoClient("mongodb+srv://alexey:alexey@cluster0.82thlib.mongodb.net/")
db = cluster["booksDB"]
collection = db["books"]



def books_get():  # noqa: E501
    """books_get

    Return all the books available in the library # noqa: E501


    :rtype: List[Book]
    """
    results = collection.find({})
    books = []
    for result in results:
        books.append(result)
        print(result["title"])


    print(books)
    # json_data = dumps(list_cur)
    return jsonify({"books": books})



def books_id_delete(id_):  # noqa: E501
    """books_id_delete

    Delete the book with the specified ID # noqa: E501

    :param id: ID of the book to delete
    :type id: str

    :rtype: None
    """
    collection.delete_one({"_id": int(id_)})
    return 'do some magic!'


def books_id_get(id_):  # noqa: E501
    """books_id_get

    Return the details about the book with the requested ID # noqa: E501

    :param id: ID of the book to request
    :type id: str

    :rtype: Book
    """

    print(id_)

    result = collection.find_one({"_id" : ObjectId(id_)})
    result["_id"] = str(result.get("_id"))
    print(result['title'])

    returned_book = Book.from_dict(result)

    return returned_book


def books_id_put(body, id_):  # noqa: E501
    """books_id_put

    Update the details about the book with the specified ID # noqa: E501

    :param body: New details of the book to be modified
    :type body: dict | bytes
    :param id: ID of the book to modify
    :type id: str

    :rtype: None
    """
    collection.update_one({"_id": int(id_)},{"$set":connexion.request.get_json()})
    return 'do some magic!'


def books_post(body):  # noqa: E501
    """books_post

    Add a new book to the library # noqa: E501

    :param body: Details of the book to add
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Book.from_dict(connexion.request.get_json()) # noqa: E501

        body.to_dict()

    # print(connexion.request.get_json())
    # TODO: try except for all mongo calls
    query_output = collection.insert_one(body.to_dict())

    if query_output.inserted_id:

        return {
            "inserted_id": str(query_output.inserted_id)
        }, 201

    else:
        raise ProblemException(
            status=500,
            detail="Error inserting New Book",
            title="Internal Server Error"
        )



def books_search_get(title=None, year=None, author=None, type_of_book=None):  # noqa: E501
    """books_search_get

    Get all the books matching your search criteria # noqa: E501

    :param title: Book title
    :type title: str
    :param year: Publication year
    :type year: int
    :param author: Book author
    :type author: str
    :param type_of_book: Type of book
    :type type_of_book: str

    :rtype: List[Book]
    """
    book = {}
    if(title): book["title"] = title
    if(year): book["year"] = year
    if(author): book["author"] = author
    if(type_of_book): book["typeOfBook"] = type_of_book

    result = collection.find_one(book)
    print(result)
    return result
