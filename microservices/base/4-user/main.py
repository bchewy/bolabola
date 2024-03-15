from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pika
import os
import json
from threading import Thread
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root@localhost:3306/user"
)

db = SQLAlchemy(app)
CORS(app)


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
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "stripe_id": self.stripe_id,
            "username": self.username,
            "password": self.password,
            "tickets": self.tickets,
        }


# path to test if the service is running
@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


# path to test if the service is running
@app.route("/", methods=["GET"])
def home():
    return "User service running"


############################################################################################################
##################################    VIEW USER TICKETS     ################################################
############################################################################################################
# view all tickets bought by the user
@app.route("/<int:id>/tickets", methods=["GET"])
def view_all_user_tickets(id):
    """
    This method returns all the tickets owned by the user.
    Query will join the User and Ticket tables and return the tickets owned by the user.
    """
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    return jsonify(user.tickets)


# view a specific ticket bought by the user by serial number
@app.route("/<int:id>/tickets/<int:serial_no>", methods=["GET"])
def view_ticket_by_serial_no(id, serial_no):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket["serial_no"] == serial_no:
            return jsonify(ticket)
    return jsonify({"message": "Ticket not found"})


# view a specific ticket bought by the user by match id
@app.route("/<int:id>/tickets/match/<int:match_id>", methods=["GET"])
def view_ticket_by_match_id(id, match_id):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket["match_id"] == match_id:
            return jsonify(ticket)
    return jsonify({"message": "Ticket not found"})


############################################################################################################
#################################    END OF VIEW USER TICKETS    ###########################################
############################################################################################################


############################################################################################################
####################################    ADD A USER TICKET     ##############################################
############################################################################################################
# add a ticket to the user's list of tickets
@app.route("/<int:id>/tickets", methods=["POST"])
def add_ticket_to_user(id, ticket):
    """
    This method adds a ticket to the user's list of tickets.
    """
    ticket = request.json
    if ticket is None:
        return jsonify({"message": "Ticket info not provided"})
    user = User.query.get(id)
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
@app.route("/<int:id>/tickets/<int:serial_no>", methods=["DELETE"])
def delete_ticket_from_user(id, serial_no):
    """
    This method deletes a ticket from the user's list of tickets.
    This will be used when the user refunds a ticket successfully.
    """
    user = User.query.get(id)
    if user is None:
        return jsonify({"message": "User not found"})
    if user.tickets is None:
        return jsonify({"message": "User has no tickets"})
    for ticket in user.tickets:
        if ticket["serial_no"] == serial_no:
            user.tickets.remove(ticket)
            db.session.commit()
            return jsonify({"message": "Ticket deleted successfully"})
    return jsonify({"message": "Ticket not found"})


############################################################################################################
####################################    END OF DELETE A USER TICKET     ####################################
############################################################################################################

############################################################################################################
######################################    RABBITMQ INFO    #################################################
############################################################################################################
# Hardcoded credentials and connection details for RabbitMQ
rabbitmq_user = "ticketboost"
rabbitmq_password = "veryS3ecureP@ssword"
rabbitmq_host = "rabbitmq"  # Name of the RabbitMQ service in Docker Compose
rabbitmq_port = 5672
rabbitmq_vhost = "/"


# Start a RabbitMQ consumer to listen for refund events
def start_rabbitmq_consumer():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        virtual_host=rabbitmq_vhost,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange="refund", exchange_type="direct", durable=True)
    channel.queue_declare(queue="user", durable=True)  # for the user service
    channel.queue_bind(exchange="refund", queue="user", routing_key="refund.user")

    def callback(ch, method, properties, body):
        # parse received message
        data = json.loads(body)
        user = User.query.get(data["user_id"])
        if user is None:
            print("User not found")
            return

        def del_ticket_from_user(user, serial_no):
            for ticket in user.tickets:
                if ticket["serial_no"] == serial_no:
                    user.tickets.remove(ticket)
                    db.session.commit()
                    print("Ticket deleted successfully")
                    return
            print("Ticket not found")

        if data["status"] == "succeeded":
            # start a new thread for database operations
            # this is because database operations are not thread safe
            refund_thread = Thread(
                target=del_ticket_from_user, args=(user, data["serial_no"])
            )
            refund_thread.start()
            print("Refund successful")
            return
        print("Refund failed")

    channel.basic_consume(queue="user", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def run_consumer_thread():
    consumer_thread = Thread(target=start_rabbitmq_consumer)
    consumer_thread.daemon = True
    consumer_thread.start()


if __name__ == "__main__":
    # run_consumer_thread()
    app.run(host="0.0.0.0", port=9004, debug=True)
