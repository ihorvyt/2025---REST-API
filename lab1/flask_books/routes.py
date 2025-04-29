from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .schemas import BookSchema

books_bp = Blueprint('books', __name__)

books = []
current_id = 1

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@books_bp.route('/books', methods=['GET'])
def get_books():
    return jsonify(books_schema.dump(books))

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book_schema.dump(book))

@books_bp.route('/books', methods=['POST'])
def add_book():
    global current_id

    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    book = {'id': current_id, **book_data}
    current_id += 1
    books.append(book)

    return jsonify(book_schema.dump(book)), 201

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message': 'Book deleted'}), 200