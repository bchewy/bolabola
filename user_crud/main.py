from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import user_schemas

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
CORS(app)

AUTH_ENDPOINT = os.environ.get('AUTH_ENDPOINT') # to create this endpoint in the future
STRIPE_ENDPOINT = os.environ.get('STRIPE_ENDPOINT') # to create this endpoint in the future

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
    Login, which returns user account object with bearer token
    """
    user = User.query.filter_by(username=user.username).first()

    # to implement legit auth in the future!!
    auth_response = request.post(f"{AUTH_ENDPOINT}/login", data={"username": user.username, "password": user.password})
    if auth_response.status_code != 200:
        raise Exception(auth_response.status_code, auth_response.text)
    token = auth_response.headers["Authorisation"]
    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid username or password"})
    
