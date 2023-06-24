from flask_login import UserMixin, current_user
from datetime import datetime



class Post:

    def __init__(self, id, title, content, date_posted = datetime.utcnow(), author = current_user):
        self.id = id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.author =  author
    

    def to_mongo(self):
        return {
            '_id': self.id,
            'title': self.title,
            'content': self.content,
            'date_posted': self.date_posted,
            'author': self.author.id
        }
