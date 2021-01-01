import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, books):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    formated_books = [book.format() for book in books]
    current_books = formated_books[start:end]
    return current_books

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

    #by default, it listens to GET request
    @app.route('/books')
    def get_books():
        all_books = Book.query.order_by(Book.id).all()
        paginated_books = paginate_books(request, all_books)

        if len(paginated_books) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'books': paginated_books,
                'total_books': len(all_books)
            })

    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        try:
            book = Book.query.get(book_id)
            if book == None:
                abort(404)

            body = request.get_json()
            if 'rating' in body:
                book.rating = int(body.get('rating'))
                book.update()
            
            return jsonify({
                'success': True,
                'book_id': book.id
            })
        except:
            abort(422)


    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.get(book_id)
            if book is None:
                abort(404)

            book.delete()
            all_remaining_books = Book.query.order_by(Book.id).all()
            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': paginate_books(request, all_remaining_books),
                'total_books': len(all_remaining_books)
            })
        except:
            abort(422)


    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.

    @app.route('/books', methods=['POST'])
    def create_book():
        try:
            json_request_body = request.get_json()
            book_title = json_request_body.get('title', None)
            book_author = json_request_body.get('author', None)
            book_rating = json_request_body.get('rating', None)
            newBook = Book(title=book_title, author=book_author, rating=int(book_rating))
            newBook.insert()
            book_id = newBook.id
            all_books = Book.query.order_by(Book.id).all()
            return jsonify({
                'success': True,
                'created': book_id,
                'books': paginate_books(request, all_books),
                'total_books': len(all_books)
            })
        except:
            abort(422)

    #error handler decorators

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Not Allowed"
        }), 405

    return app