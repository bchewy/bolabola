from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import user_schemas, user_crud

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
CORS(app)

AUTH_ENDPOINT = os.environ.get('AUTH_ENDPOINT') # to create this endpoint in the future
STRIPE_ENDPOINT = os.environ.get('STRIPE_ENDPOINT') # to create this endpoint in the future

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    stripe_id = db.Column(db.String(120), unique=True, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# route to create a new account
@app.route('/createAccount', methods=['POST'])
def create_account(user: user_schemas.UserAccountCreate):
    """
    Create a new account by providing the user's name, email, username, password
    """
    new_user = User(name=user.name, email=user.email, username=user.username, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Account created successfully"})

# route to login
@app.route('/login', methods=['POST'])
def login(user: user_schemas.UserLogin):
    """
    Login
    """
    user = user_crud.get_user(user)
    if user is None:
        return jsonify({"message": "Invalid credentials"})
    return user
