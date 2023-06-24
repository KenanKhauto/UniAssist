from application.extensions import mongo
from .models import Post

class PostRepository:


    def insert_post(self, title, content):
        # create id for post
        existing_ids = mongo.db.posts.distinct('_id')
        available_ids = set(range(1, max(existing_ids, default=0) + 2)) - set(existing_ids)
        post_id = min(available_ids)

        post = Post(id=post_id, title=title, content=content)  
        mongo.db.posts.insert_one(post.to_mongo())
        return post
    
    def find_posts(self):
        posts = []
        for post_data in mongo.db.posts.find():
            posts.append(Post(title=post_data['title'], content=post_data['content'], author=post_data['author'], date_posted=post_data['date_posted'], id=post_data['_id']))
        return posts
    

