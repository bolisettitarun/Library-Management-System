# Define a class `Book` with attributes title, author, and ISBN
class Book():
    def __init__(self, title, author, ISBN):
        if not isinstance(title, str) or not isinstance(author, str) or not isinstance(ISBN, int):
            raise TypeError("Invalid input types. Title and author must be strings, ISBN must be an integer.")
        self.title = title
        self.author = author
        self.ISBN = ISBN

    # Method to display details of the book
    def display(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.ISBN}")

# Define a class `Library` to manage a collection of books
class Library():
    def __init__(self):
        self.books = []  # Initialize an empty list to store books

    # Method to add a book to the library
    def add_book(self, book):
        if isinstance(book, Book):  # Check if the parameter is an instance of Book
            self.books.append(book)
        else:
            print("Expected an instance of book")

    # Method to display all books in the library
    def display_books(self):
        if not self.books:
            print("No books in the library")
        else:
            for book in self.books:
                book.display()  # Call the display method of each book
                print("------")  # Separate each book's details with a line

    # Method to search for a book by title
    def search_book_by_title(self, title):
        found_books = []
        try:
            for book in self.books:
                if book.title.lower() == title.lower():
                    found_books.append(book)
            if not found_books:
                print(f"No book with title '{title}' found")
            else:
                for book in found_books:
                    book.display()
                    print("------")
        except AttributeError:
            print("Error: Book object has no attribute 'title'")

# Define a subclass `Ebook` of `Book` with an additional attribute `file_format`
class Ebook(Book):
    def __init__(self, title, author, ISBN, file_format):
        if not isinstance(file_format, str):
            raise TypeError("File format must be a string.")
        super().__init__(title, author, ISBN)  # Call the superclass constructor
        self.file_format = file_format  # Initialize the file format attribute

    # Override the display method to include file format
    def display(self):
        super().display()  # Call the display method of the superclass
        print(f"File format: {self.file_format}")  # Print the file format

# Creating instances of Book, Ebook, and Library
book1 = Book("one", "one", 1)
book2 = Book("two", "two", 2)
ebook1 = Ebook("three", "three", 3, "pdf")
library = Library()  # Create a library instance

# Adding books to the library
library.add_book(book1)
library.add_book(book2)
library.add_book(ebook1)

# Displaying all books in the library
library.display_books()

# Searching for a book by title
library.search_book_by_title("two")


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configure the database URI. Change the database connection string as per your setup.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/scott'
db = SQLAlchemy(app)
app.app_context().push()

# Define the Book model
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    ISBN = db.Column(db.String(13), unique=True)

    # Method to convert Book object to dictionary for JSON serialization
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'ISBN': self.ISBN
        }
    
# Define the EBook model with a relationship to Book
class EBook(db.Model):
    __tablename__ = 'ebooks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship('Book')
    format = db.Column(db.String(10))  # e.g., PDF, EPUB

    # Method to convert EBook object to dictionary for JSON serialization
    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.to_dict(),  # Include Book details in the dictionary
            'format': self.format
        }

# Endpoint to handle GET and POST requests for /books
@app.route('/books', methods=['GET', 'POST'])
def book_list():
    if request.method == 'GET':
        # Retrieve all books from the database and return them as JSON
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])

    elif request.method == 'POST':
        try:
            # Extract JSON data from the request and create a new Book object
            data = request.get_json()
            book = Book(title=data['title'], author=data['author'], ISBN=data['ISBN'])

            # Add the Book object to the database session and commit the transaction
            db.session.add(book)
            db.session.commit()

            # Return the newly created Book object as JSON with status code 201 (Created)
            return jsonify(book.to_dict()), 201

        except (KeyError, IntegrityError) as e:
            # Handle errors such as missing JSON keys or IntegrityError (e.g., unique constraint violation)
            return jsonify({'error': str(e)}), 400  # Bad Request

# Endpoint to handle GET and DELETE requests for /books/<book_id>
@app.route('/books/<int:book_id>', methods=['GET', 'DELETE'])
def book_detail(book_id):
    # Retrieve the Book object by its ID
    book = Book.query.get(book_id)

    if not book:
        # Return error JSON if the book with the specified ID is not found
        return jsonify({'error': 'Book not found'}), 404  # Not Found

    if request.method == 'GET':
        # Return the details of the Book object as JSON
        return jsonify(book.to_dict())

    elif request.method == 'DELETE':
        # Delete the Book object from the database session and commit the transaction
        db.session.delete(book)
        db.session.commit()

        # Return success message as JSON with status code 204 
        return jsonify({'message': 'Book deleted'}), 204

# Endpoint to handle GET and POST requests for /ebooks
@app.route('/ebooks', methods=['GET', 'POST'])
def ebook_list():
    if request.method == 'GET':
        # Retrieve all EBooks with associated Book details efficiently using join
        ebooks = EBook.query.join(Book).all()
        return jsonify([ebook.to_dict() for ebook in ebooks])

    elif request.method == 'POST':
        try:
            # Extract JSON data from the request and create a new Book and EBook object
            data = request.get_json()
            book = Book(title=data['title'], author=data['author'], ISBN=data['ISBN'])
            ebook = EBook(book=book, format=data['format'])

            # Add the Book and EBook objects to the database session and commit the transaction
            db.session.add(book)  # Add Book first due to foreign key constraint
            db.session.add(ebook)
            db.session.commit()

            # Return the newly created EBook object as JSON with status code 201 (Created)
            return jsonify(ebook.to_dict()), 201

        except (KeyError, IntegrityError) as e:
            # Handle errors such as missing JSON keys or IntegrityError (e.g., unique constraint violation)
            return jsonify({'error': str(e)}), 400  # Bad Request

if __name__ == '__main__':
    # Create all database tables defined in the models
    db.create_all()
    app.run(debug=True)






