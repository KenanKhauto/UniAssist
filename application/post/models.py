from flask_login import current_user
from datetime import datetime




class Post:

    def __init__(self, id, title, content, date_posted = datetime.utcnow(), author = current_user):
        self.id = id
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.author =  author
    

    @classmethod
    def from_mongo(cls, mongo_doc):
        id = mongo_doc['_id']
        title = mongo_doc['title']
        content = mongo_doc['content']
        date_posted = mongo_doc['date_posted']
        author_id = mongo_doc['author']
        from application.custom import user_rep
        # Retrieve author from MongoDB 
        author = user_rep.find_user_by_id(author_id) 

        return cls(id=id, title=title, content=content, date_posted=date_posted, author=author)


    def to_mongo(self):
        return {
            '_id': self.id,
            'title': self.title,
            'content': self.content,
            'date_posted': self.date_posted,
            'author': self.author.id
        }
