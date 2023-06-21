from application.extensions import mongo
from .models import User, Book

class UserRepository:
    """
    Repository class for user-related operations.

    Attributes:
        None
    """

    def __init__(self):
        """
        Initializes the UserRepository object.

        Args:
            None
        """
        pass

    def find_user_by_id(self, user_id):
        """
        Find a user by their ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            User: The User object if the user is found, otherwise None.
        """
        user_data = mongo.db.users.find_one({'_id': user_id})
        if user_data:
            return User(user_data)
        return None

    def find_user_by_username(self, username):
        """
        Find a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The User object if the user is found, otherwise None.
        """
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None
    
    def find_user_by_email(self, email):
        """
        Find a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The User object if the user is found, otherwise None.
        """
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

    def register_user(self, username, password, email):
        """
        Register a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            email (str): The email of the user.

        Returns:
            User: The registered User object.
        """
        # Find the lowest available ID
        existing_ids = mongo.db.users.distinct('_id')
        available_ids = set(range(1, max(existing_ids, default=0) + 2)) - set(existing_ids)
        user_id = min(available_ids)

        user_data = {'_id': user_id, 'username': username, 'password': password, 'email': email, 'image_file' : 'default.jpg'}
        mongo.db.users.insert_one(user_data)

        user = User(user_data)
        return user
    
    def create_indexes(self):
        """
        Create indexes for the 'username' and 'email' fields in the users collection.

        Args:
            None

        Returns:
            None
        """
        mongo.db.users.create_index("username", unique=True)
        mongo.db.users.create_index("email", unique=True)


    def update_user_username(self, user):
        filter = {'_id': user.id}
        new_username = {"$set" : {"username" : user.username}} 
        mongo.db.users.update_one(filter, new_username)

    def update_user_email(self, user):
        filter = {'_id': user.id}
        new_email = {"$set" : {"email" : user.email}} 
        mongo.db.users.update_one(filter, new_email)

    def update_user_image(self, user):
        filter = {'_id': user.id}
        new_image = {"$set" : {"image_file" : user.image_file}} 
        mongo.db.users.update_one(filter, new_image)








class BookRepository:
    

    def find_book_by_id(self, book_id):
        book_data = mongo.db.books.find_one({'_id': book_id})
        print(book_data)
        if book_data:
            return Book(book_data)
        return None

    def find_book_by_name(self, name):
        book_data = mongo.db.books.find_one({'book_name':name})
        if book_data:
            return Book(book_data)
        return None
    
    def find_books_per_user(self, user_id):
        book_data = mongo.db.books.find({'user_id':user_id})
        if book_data:
            books_list = []
            for book in book_data:
                book_obj = Book(book)
                books_list.append(book_obj)
            return books_list
        return None

    def save_book_in_DB(self, book_data):
        check_for_book = self.find_book_by_id(book_data["_id"])
        if check_for_book:
            return None
        
        
        inserted_book = mongo.db.books.insert_one(book_data)
        book_id = inserted_book.inserted_id


        user_id = book_data["user_id"]
        mongo.db.users.update_one({"_id": user_id}, {"$push": {"books_ids": book_id}})

        book_data["_id"] = book_id
        book = Book(book_data)
        return book
    
    def delete_book_from_DB_by_name(self, book_name):
        mongo.db.books.delete_one({'book_name':book_name})
    
    def delete_book_from_DB_by_id(self, book_id):
        mongo.db.books.delete_one({'_id':book_id})

    def get_notes(self, book_id):
        book_data = self.find_book_by_id(book_id)
        if book_data:
            return book_data["notes"]
        return None
    
    def delete_note_from_DB(self, book_id, note_id):
        book_data = self.find_book_by_id(book_id)
        if book_data:
            notes = book_data["notes"]
            for note in notes:
                if note["note_id"] == note_id:
                    notes.remove(note)
                    break
            filter = {'_id': book_id}
            new_notes = {"$set" : {"notes" : notes}} 
            mongo.db.books.update_one(filter, new_notes)
            return True
        return False