
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['_id']
        self.username = user_data['username']
        self.password = user_data['password']
        self.email = user_data['email']

    def to_json(self):
        return {
            '_id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        