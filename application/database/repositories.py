
from application.extensions import mongo
from .models import User


## add more methods later like delete etc..

class UserRepository:
    def __init__(self):
        pass

    def find_user_by_id(self, user_id):
        user_data = mongo.db.users.find_one({'_id': user_id})
        if user_data:
            return User(user_data)
        return None

    def find_user_by_username(self, username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None
    
    def find_user_by_email(self, email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

    def register_user(self, username, password, email):
        user_data = {'username': username, 'password': password, 'email': email}
        result = mongo.db.users.insert_one(user_data)
        user_id = str(result.inserted_id)
        user_data['_id'] = user_id
        user = User(user_data)
        return user.to_json()
    
    def create_indexes(self):
        mongo.db.users.create_index("username", unique=True)
        mongo.db.users.create_index("email", unique=True)