from flask_login import UserMixin, current_user
from datetime import datetime


class User(UserMixin):
    """
    User class representing a user object.

    This class extends Flask-Login's UserMixin to provide additional user-related functionality.

    Attributes:
        id (str): The ID of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email of the user.
    """

    def __init__(self, user_data):
        """
        Initializes a User object.

        Args:
            user_data (dict): User data containing the user's attributes.

        Returns:
            None
        """
        self.id = user_data['_id']
        self.username = user_data['username']
        self.password = user_data['password']
        self.email = user_data['email']
        self.image_file = user_data['image_file']
       

    def to_json(self):
        """
        Converts the User object to a JSON representation.

        Args:
            None

        Returns:
            dict: JSON representation of the User object.
        """
        return {
            '_id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'image_file':self.image_file
        }
    

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
