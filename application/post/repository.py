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
            posts.append(Post.from_mongo(post_data))
        return posts
    
    def find_post_by_id(self, post_id):
        post_data = mongo.db.posts.find_one({'_id': post_id})
        return Post.from_mongo(post_data)
    
    def update_post(self, post, title, content):

        post.title = title
        post.content = content
        mongo.db.posts.update_one({'_id': post.id}, {'$set': post.to_mongo()})
        return post

