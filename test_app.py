import unittest
from app import app, mongo, bcrypt
from flask import json
from flask_jwt_extended import create_access_token

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Set up the test client and initialize test database
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = "mongodb://localhost:27017/blogs"
        self.client = app.test_client()
        with app.app_context():
            mongo.db.users.drop()
            mongo.db.posts.drop()

    def test_signup(self):
        # Test user registration
        response = self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        print('Signup Response:', response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registered successfully', response.get_data(as_text=True))

    def test_login(self):
        # Register and then login
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        print('Login Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_upload_image(self):
        # Register, login, and then upload an image
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        with open('test_image.jpg', 'rb') as img:
            response = self.client.post('/upload-image', 
                                        data={'file': img}, 
                                        headers={'Authorization': f'Bearer {token}'},
                                        content_type='multipart/form-data')
        print('Upload Image Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('image_base64', response.get_json())

    def test_create_blogpost(self):
        # Register, login, and then create a blog post
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        response = self.client.post('/blogposts', 
                                    data={'title': 'Test Post', 'content': 'This is a test post'}, 
                                    headers={'Authorization': f'Bearer {token}'})
        print('Create Blogpost Response:', response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Blog post created', response.get_data(as_text=True))

    def test_get_blogposts(self):
        # Register, login, create a post, and then get all posts
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        self.client.post('/blogposts', 
                         data={'title': 'Test Post', 'content': 'This is a test post'}, 
                         headers={'Authorization': f'Bearer {token}'})
        
        response = self.client.get('/blogposts')
        print('Get Blogposts Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

    def test_get_blogpost(self):
        # Register, login, create a post, and then get the post by ID
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        create_response = self.client.post('/blogposts', 
                                           data={'title': 'Test Post', 'content': 'This is a test post'}, 
                                           headers={'Authorization': f'Bearer {token}'})
        post_id = create_response.get_json()['post_id']

        response = self.client.get(f'/blogposts/{post_id}')
        print('Get Blogpost Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.get_json())
        self.assertIn('content', response.get_json())

    def test_update_blogpost(self):
        # Register, login, create a post, and then update the post
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        create_response = self.client.post('/blogposts', 
                                           data={'title': 'Test Post', 'content': 'This is a test post'}, 
                                           headers={'Authorization': f'Bearer {token}'})
        post_id = create_response.get_json()['post_id']

        response = self.client.put(f'/blogposts/{post_id}', 
                                   data={'title': 'Updated Post', 'content': 'Updated content'}, 
                                   headers={'Authorization': f'Bearer {token}'})
        print('Update Blogpost Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Blog post updated', response.get_data(as_text=True))

    def test_delete_blogpost(self):
        # Register, login, create a post, and then delete the post
        self.client.post('/signup', json={'username': 'testuser', 'password': 'testpass'})
        login_response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpass'})
        token = login_response.get_json()['access_token']

        create_response = self.client.post('/blogposts', 
                                           data={'title': 'Test Post', 'content': 'This is a test post'}, 
                                           headers={'Authorization': f'Bearer {token}'})
        post_id = create_response.get_json()['post_id']

        response = self.client.delete(f'/blogposts/{post_id}', 
                                      headers={'Authorization': f'Bearer {token}'})
        print('Delete Blogpost Response:', response.json)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Blog post deleted', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main(verbosity=2)
