from flask_login import UserMixin, current_user
from datetime import datetime
from application.extensions import mongo


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
        self.followers = user_data.get('followers', [])
        self.following = user_data.get('following', [])

    
    def follow(self, user):
        if user.id not in self.following:
            self.following.append(user.id)
            user.followers.append(self.id)
            mongo.db.users.update_one({'_id': self.id}, {'$push': {'following': user.id}})
            mongo.db.users.update_one({'_id': user.id}, {'$push': {'followers': self.id}})
    
    def unfollow(self, user):
        if user.id in self.following:
            self.following.remove(user.id)
            user.followers.remove(self.id)
            mongo.db.users.update_one({'_id': self.id}, {'$pull': {'following': user.id}})
            mongo.db.users.update_one({'_id': user.id}, {'$pull': {'followers': self.id}})
    
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
            'image_file': self.image_file,
            'followers': self.followers,
            'following': self.following
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
