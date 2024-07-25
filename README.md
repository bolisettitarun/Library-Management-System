# Library-Management-System
 A comprehensive repository for managing library operations, including book adding, fetching, and deleting a book
This project implements a library management system using Python and Flask, with SQLAlchemy for database management. It allows for managing both physical books and ebooks, providing endpoints for CRUD operations via a RESTful API.

Features
Book and Ebook Classes: Define classes for Book and Ebook, with attributes like title, author, ISBN, and additional attributes for ebooks like file format.

Library Class: Manages a collection of books (Book instances), with methods to add books, display all books, and search books by title.

Flask RESTful API: Implements endpoints for:

Retrieving all books (GET /books)
Adding a new book (POST /books)
Retrieving, updating, and deleting a specific book (GET /books/<book_id>, DELETE /books/<book_id>)
Retrieving all ebooks with associated book details (GET /ebooks)
Adding a new ebook (POST /ebooks)
Database Integration: Uses MySQL database (configured in the Flask app) with SQLAlchemy ORM for defining models (Book and EBook) and managing database operations.

Getting Started
Prerequisites
Python 3.x
Flask (pip install Flask)
SQLAlchemy (pip install SQLAlchemy)
MySQL (or another database supported by SQLAlchemy)



Configure the database URI in app.py:

SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/database_name'

Run the Flask application:
python app.py

The API endpoints will be accessible at http://localhost:5000.
API Endpoints
GET /books: Retrieve all books.
POST /books: Add a new book.
GET /books/<book_id>: Retrieve details of a specific book.
DELETE /books/<book_id>: Delete a specific book.
GET /ebooks: Retrieve all ebooks with associated book details.
POST /ebooks: Add a new ebook.

Examples

Adding a Book
'{"title":"Book Title","author":"Author Name","ISBN":"1234567890123"}' http://localhost:5000/books

Retrieving All Books
http://localhost:5000/books

Deleting a Book
http://localhost:5000/books/<book_id>
