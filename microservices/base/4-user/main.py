from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import os

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
    tickets = db.Column(db.JSON, nullable=True)

    def __init__(self, id, name, email, stripe_id, username, password, tickets=None):
        self.id = id
        self.name = name
        self.email = email
        self.stripe_id = stripe_id
        self.username = username
        self.password = password
        self.tickets = tickets

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "stripe_id": self.stripe_id, "username": self.username, "password": self.password, "tickets": self.tickets}

############################################################################################################
##################################    VIEW USER TICKETS     ################################################
############################################################################################################
# view all tickets bought by the user
@app.route("/api/v1/user/<int:id>/tickets", methods=["GET"])
def view_all_user_tickets(self):
        """
        This method returns all the tickets owned by the user.
        Query will join the User and Ticket tables and return the tickets owned by the user.
        """
        return jsonify(self.tickets)

# view a specific ticket bought by the user by serial number  
@app.route("/api/v1/user/<int:id>/tickets/<int:serial_no>", methods=["GET"])  
def view_ticket_by_serial_no(self, serial_no):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    user = User.query.get(self.id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket['serial_no'] == serial_no:
            return jsonify(ticket)
    return jsonify({"message": "Ticket not found"})
    
# view a specific ticket bought by the user by match id
@app.route("/api/v1/user/<int:id>/tickets/match/<int:match_id>", methods=["GET"])
def view_ticket_by_match_id(self, match_id):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    user = User.query.get(self.id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket['match_id'] == match_id:
            return jsonify(ticket)
    return jsonify({"message": "Ticket not found"})

############################################################################################################
#################################    END OF VIEW USER TICKETS    ###########################################
############################################################################################################


############################################################################################################
####################################    ADD A USER TICKET     ##############################################
############################################################################################################
# add a ticket to the user's list of tickets
@app.route("/api/v1/user/<int:id>/tickets", methods=["POST"])
def add_ticket_to_user(self, ticket):
    """
    This method adds a ticket to the user's list of tickets.
    """
    user = User.query.get(self.id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        user.tickets = []
    user.tickets.append(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket added successfully"})

############################################################################################################
####################################    END OF ADD A USER TICKET     #######################################
############################################################################################################

############################################################################################################
####################################    DELETE A USER TICKET     ###########################################
############################################################################################################
# delete a ticket from the user's list of tickets
@app.route("/api/v1/user/<int:id>/tickets/<int:serial_no>", methods=["DELETE"])
def delete_ticket_from_user(self, serial_no):
    """
    This method deletes a ticket from the user's list of tickets.
    This will be used when the user refunds a ticket successfully.
    """
    user = User.query.get(self.id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket['serial_no'] == serial_no:
            user.tickets.remove(ticket)
            db.session.commit()
            return jsonify({"message": "Ticket deleted successfully"})
    return jsonify({"message": "Ticket not found"})

############################################################################################################
####################################    END OF DELETE A USER TICKET     ####################################
############################################################################################################

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9004, debug=True)