from application.extensions import mongo
from .models import User
from application.tasks.models import Task

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

    def create_search_index(self):
        mongo.db.users.create_index([('username', 'text'), ('email', 'text')])

    def search_users(self, query):
        if query is None or query == '':
            return []
        else:
            users = []
            for user_data in mongo.db.users.find({'$text': {'$search': query}}):
                users.append(User(user_data))
            return users
        
    # add one task to list field "my_tasks" with task and user id
    def add_task_by_user_id(self, user, description):
        # get id of last task
        try:
            tasks_ls = mongo.db.users.find_one({'_id': user.id})['my_tasks']
        except:
            tasks_ls = None           
        task_id = 1

        if tasks_ls:
            last_task_id = mongo.db.users.find_one({'_id': user.id})['my_tasks'][-1]['_id']
            task_id = last_task_id + 1

        task_dic = {'_id': task_id, 'description': description, 'status': 'Todo'}
        task = Task(task_dic)
        filter = {'_id': user.id}
        new_task = {"$push" : {"my_tasks" : task.to_mongo()}}
        mongo.db.users.update_one(filter, new_task)
    
    # update task status
    def update_task_status(self, task_id, user, status):
        filter = {'_id': user.id}
        new_task = {"$set" : {"my_tasks.$[elem].status" : status}} 
        mongo.db.users.update_one(filter, new_task, array_filters=[{"elem._id": task_id}])

    # delete task from list field "my_tasks" with task and user id
    def delete_task_from_user_by_id(self, user, task_id):
        filter = {'_id': user.id}
        new_task = {"$pull" : {"my_tasks" : {"_id":task_id}}} 
        mongo.db.users.update_one(filter, new_task)

    # find all tasks of user
    def find_tasks_by_user_id(self, user):
        user_id = user.id
        try:
            tasks = []
            for data in mongo.db.users.find_one({'_id': user_id})['my_tasks']:
                tasks.append(Task(data))
        except:
            return None
        
        return tasks
    
    def update_task_description(self, task_id,  user, description):
        filter = {'_id': user.id}
        new_task = {"$set" : {"my_tasks.$[elem].description" : description}} 
        mongo.db.users.update_one(filter, new_task, array_filters=[{"elem._id": task_id}])


    def get_following_list_by_id(self, user):
        filter = {"_id": user.id}
        
        user_data = mongo.db.users.find_one(filter, {'following': 1})

        # Check if the user_data contains the 'following' field
        if user_data and 'following' in user_data:
            # Return the list of user IDs that this user is following
            return user_data['following']
        else:
            # Return an empty list if the 'following' field is not found
            return []
        
    def get_following_as_list_of_users(self, user):

        following_list = self.get_following_list_by_id(user)
        u_list = []

        if following_list:
            for id in following_list:
                user_ = self.find_user_by_id(id)
                if user_:
                    u_list.append(user_)
                
        return u_list