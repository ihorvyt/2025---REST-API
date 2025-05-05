from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import BookSchema, PaginationSchema
from app.models import Book
from app import db

books_bp = Blueprint('books', __name__)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
pagination_schema = PaginationSchema()

@books_bp.route('/books', methods=['GET'])
def get_books():
    limit = request.args.get('limit', 10, type=int)
    cursor = request.args.get('cursor', type=int)

    if limit > 100:
        limit = 100

    books_query = Book.query.order_by(Book.id)

    if cursor:
        books_query = books_query.filter(Book.id > cursor)

    books = books_query.limit(limit).all()
    next_cursor = books[-1].id if books else None

    result = {
        'items': [book.to_dict() for book in books],
        'next_cursor': next_cursor,
        'limit': limit
    }

    return jsonify(result)

@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@books_bp.route('/books', methods=['POST'])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    book = Book(
        title=book_data['title'],
        author=book_data['author']
    )
    
    db.session.add(book)
    db.session.commit()
    
    return jsonify(book.to_dict()), 201

@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    book.title = book_data['title']
    book.author = book_data['author']
    
    db.session.commit()
    
    return jsonify(book.to_dict())

@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'message': 'Book deleted'}), 200