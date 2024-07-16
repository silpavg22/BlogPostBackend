from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
app = Flask(__name__)

# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/blogs"
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a more secure key in production

jwt = JWTManager(app)

# Initialize MongoDB, Bcrypt, and HTTPAuth
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth(app)
CORS(app)

from . import routes, auth
