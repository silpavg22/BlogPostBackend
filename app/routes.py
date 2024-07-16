import os
import base64
from flask import Flask, request, Response, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json
from bson import ObjectId
from app import app
from .models import BlogPost, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from . import app, bcrypt

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")

@app.route('/test')
def test():
    return 'The Flask app is working!'

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json['username']
    password = request.json['password']
    if User.create_user(username, password):
        return jsonify({'message': 'Registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Authenticate user
    user = User.get_user(username)
    if user and bcrypt.check_password_hash(user['password'], password):
        # Create JWT token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "The username or password is incorrect"}), 401

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        return jsonify({'image_base64': encoded_string}), 200
    return jsonify({'message': 'Invalid file type'}), 400

@app.route('/blogposts', methods=['POST'])
@jwt_required()
def create_blogpost():
    try:
        # Extract data from request
        title = request.form['title']
        content = request.form['content']
        author = get_jwt_identity()
        image_url = ''
        image_base64 = ''
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                with open(file_path, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Attempt to create a blog post
        inserted_id = BlogPost.create_post(title, content, author, image_base64)
        if inserted_id:
            return jsonify({'message': 'Blog post created', 'post_id': str(inserted_id)}), 201
        else:
            return jsonify({'message': 'Creation failed'}), 400
    except KeyError as e:
        return jsonify({'message': f'Missing key in request data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/blogposts', methods=['GET'])
def get_blogposts():
    posts = BlogPost.get_posts()
    json_posts = json.dumps(posts, default=json_encoder)
    return Response(json_posts, mimetype='application/json'), 200

@app.route('/blogposts/<post_id>', methods=['GET'])
def get_blogpost(post_id):
    post = BlogPost.get_post(post_id)
    if post:
        post['_id'] = str(post['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(post), 200
    return jsonify({'message': 'Post not found'}), 404

@app.route('/blogposts/<post_id>', methods=['PUT'])
@jwt_required()
def update_blogpost(post_id):
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        image_base64 = ''
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                with open(file_path, "rb") as image_file:
                    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        if title is None or content is None:
            return jsonify({'message': 'Title or content missing'}), 400
        
        if BlogPost.update_post(post_id, title, content, image_base64):
            return jsonify({'message': 'Blog post updated'}), 200
        else:
            return jsonify({'message': 'Update failed, no changes made'}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/blogposts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_blogpost(post_id):
    if BlogPost.delete_post(post_id):
        return jsonify({'message': 'Blog post deleted'}), 200
    return jsonify({'message': 'Deletion failed'}), 400

@app.route('/images/<path:filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
