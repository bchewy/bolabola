from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import os
import user_schemas, user_crud, ticket_schemas

app = Flask(__name__)
if 'WAMP' in os.environ:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('mysql+mysqlconnector://root@localhost:3306/ticketboost_user')
    app.config["SQLALCHEMY_BINDS"] = {
        'ticket_db': os.environ.get('mysql+mysqlconnector://root@localhost:3306/ticketboost_ticket')  # Another database URI
    }
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('mysql+mysqlconnector://root:root@localhost:3306/ticketboost_user')
    app.config["SQLALCHEMY_BINDS"] = {
        'ticket_db': os.environ.get('mysql+mysqlconnector://root:root@localhost:3306/ticketboost_ticket')  # Another database URI
    }
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
    tickets = db.relationship(db.JSON, nullable=False)

    def __init__(self, id, name, email, stripe_id, username, password, tickets=None):
        self.id = id
        self.name = name
        self.email = email
        self.stripe_id = stripe_id
        self.username = username
        self.password = password
        self.tickets = tickets if tickets else {}

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "stripe_id": self.stripe_id, "username": self.username, "password": self.password, "tickets": self.tickets}
    
    def view_all_tickets(self):
        """
        This method returns all the tickets owned by the user.
        Query will join the User and Ticket tables and return the tickets owned by the user.
        """
        return jsonify(self.tickets)

    def view_ticket(self, ticket_id):
        """
        This method returns the details of a specific ticket owned by the user.
        """
        user = User.query.get(self.id)
        if user is None:
            return jsonify({"message": "User not found"})

        if ticket_id not in user.tickets:
            return jsonify({"message": "Ticket not found"})
        
        return jsonify(user.tickets[ticket_id])

# route to create a new account
@app.route('/api/v1/createAccount', methods=['POST'])
def create_account(user: user_schemas.UserAccountCreate):
    """
    Create a new account by providing the user's name, email, username, password
    """
    new_user = User(name=user.name, email=user.email, username=user.username, password=user.password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Account created successfully"})

# route to login
@app.route('/api/v1/login', methods=['POST'])
def login(user: user_schemas.UserLogin):
    """
    Login
    Returns the user's details if the credentials are correct
    """
    user = user_crud.get_user(user)
    if user is None:
        return jsonify({"message": "Invalid credentials"})
    return user

# view tickets bought by specific user 
@app.route('/api/v1/user/<int:user_id>/tickets', methods=['GET'])
def view_user_tickets(user_id):
    """
    View all tickets owned by a specific user
    """
    user = user_crud.get_user(user_id)
    if user is None:
        return jsonify({"message": "User not found"})
    return user.view_all_tickets()

# view ticket details
@app.route('/api/v1/user/<int:user_id>/tickets/<int:ticket_id>', methods=['GET'])
def view_ticket(user_id, ticket_id):
    """
    View the details of a specific ticket owned by a specific user
    """
    user = user_crud.get_user(user_id)
    if user is None:
        return jsonify({"message": "User not found"})
    return user.view_ticket(ticket_id)

# route to add ticket to user
@app.route('/api/v1/user/<int:user_id>/tickets/add', methods=['POST'])
def add_ticket_to_user(user_id, match_id, ticket_category, ticket_id):
    """
    Add a ticket to a specific user
    """
    user = user_crud.get_user(user_id)
    if user is None:
        return jsonify({"message": "User not found"})

    try:
        # Adding ticket details directly to the user's tickets dictionary
        user.add_ticket(match_id, ticket_category, ticket_id)
        db.session.commit()
        return jsonify({"message": f"Ticket added successfully to user {user_id}."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add Ticket."})

# NOT SURE IF THIS IS NEEDED
# route to change ticket details
@app.route("/ticket/<int:ticket_id>/edit", methods = ["UPDATE"])
def change_ticket_details(user_id, ticket_id):
    try:
        new_details = request.json
        ticket = ticket_schemas.get_ticket(user_id, ticket_id)
        ticket.event_id = new_details["event_id"]
        ticket.venue_id = new_details["venue_id"]
        ticket.seat_id = new_details["seat_id"]
        ticket.purchased_at = new_details["purchased_at"]
        return jsonify({'message': 'Ticket details updated successfully.'})
    except Exception as e:
        code = 500
        return jsonify({"code": code,"message": "Error when changing ticket details."})

# route to delete ticket
@app.route("/ticket/<int:ticket_id>/del", methods = ["DELETE"])
def delete_ticket(user_id, ticket_id):
    try:
        ticket = ticket_schemas.TicketModel.query.get(ticket_id)
        if ticket:
            # If the ticket exists, delete it from the database
            db.session.delete(ticket)
            db.session.commit()
            return jsonify({'message': f'Ticket with ID {ticket_id} has been deleted successfully.'})
        else:
            return jsonify({"message": "Ticket already deleted."})
        
    except Exception as e:
        code = 500
        return jsonify({"code": code, "message": "Unable to delete ticket"})

# route to view all tickets 
@app.route('/tickets', methods=['GET'])
def view_user_tickets(user_id):
    try:
        tickets = user_crud.get_all_tickets(user_id)
        # Convert TicketOwned objects to dictionaries before jsonify
        tickets_dict = [ticket.dict() for ticket in tickets]
        return jsonify(tickets_dict)
    except Exception as e:
        code = 500
        return jsonify({"code": code, 'message': "Failed to view all tickets."})

# route to see ticket details
@app.route("/tickets/<int:ticket_id>", methods = ["GET"])
def view_ticket(user_id, ticket_id):
    try:
        ticket = user_crud.get_ticket(user_id, ticket_id)
        return ticket
    except Exception as e:
        code = 500
        return jsonify({"code": code, 'message': "Failed to access ticket."})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9004, debug=True)