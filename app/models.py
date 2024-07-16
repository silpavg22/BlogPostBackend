from app import mongo, bcrypt
from bson import ObjectId
from pymongo.errors import PyMongoError

class User:
    @staticmethod
    def create_user(username, password):
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = mongo.db.users.insert_one({'username': username, 'password': password_hash}).inserted_id
        return user_id

    @staticmethod
    def exists(username):
        return mongo.db.users.find_one({'username': username}) is not None

    @staticmethod
    def get_user(username):
        user = mongo.db.users.find_one({"username": username})
        return user

class BlogPost:
    @staticmethod
    def create_post(title, content, author, image_url):
        post = {
            'title': title,
            'content': content,
            'author': author,
            'image_url': image_url
        }
        result = mongo.db.posts.insert_one(post)
        return result.inserted_id

    @staticmethod
    def get_posts():
        return list(mongo.db.posts.find())

    @staticmethod
    def get_post(post_id):
        try:
            result = mongo.db.posts.find_one({'_id': ObjectId(post_id)})
            print(f"Queried result for {post_id}: {result}")  # Debug output
            return result
        except PyMongoError as e:
            print("Error accessing the database:", e)
            return None

    @staticmethod
    def update_post(post_id, title, content, image_url):
        update_data = {
            'title': title,
            'content': content,
            'image_url': image_url
        }
        result = mongo.db.posts.update_one(
            {'_id': ObjectId(post_id)}, 
            {'$set': update_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_post(post_id):
        result = mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count > 0
