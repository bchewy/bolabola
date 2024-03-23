# from flask import Flask, jsonify, request

import quart_flask_patch
from quart import Quart, jsonify, request


# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, Column, Integer, String, JSON, select
from sqlalchemy.orm.attributes import flag_modified

# SQLAlchemy Asynchronous
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Others
import pika
import os
import json
from threading import Thread
from flask_cors import CORS

# Asynchronous things
import asyncio
import aio_pika
import aiomysql


## AMQP items ################################################################################################
async def on_message(message: aio_pika.IncomingMessage):
    """
    Sample data received after json.loads(message.body.decode()):
    {
        "user_id": "auth0|1234",
        "match_id": "1",
        "category": "A",
        "serial_no": "100",
        "payment_intent": "pi_1J3s4aJGdJy1w4fF3"
    }
    """
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        data = json.loads(message.body.decode())
        user_id = data["user_id"]
        match_id = data["match_id"]
        category = data["category"]
        serial_no = data["serial_no"]
        payment_intent = data["payment_intent"]

        # Add the ticket into the user's database
        async with AsyncSessionLocal() as session:
            async with session.begin():
                user = await session.get(User, user_id)
                if user is None:
                    print("User not found")
                    return
                if user.tickets is None:
                    user.tickets = [{"match_id": match_id, "ticket_category": category, "serial_no": serial_no, "payment_intent": payment_intent}]
                else:
                    user.tickets.append({"match_id": match_id, "ticket_category": category, "serial_no": serial_no, "payment_intent": payment_intent})
                flag_modified(user, "tickets")
                await session.commit()
                print("Ticket added successfully")

async def amqp():
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()

    exchange = await channel.declare_exchange("booking", aio_pika.ExchangeType.DIRECT, durable=True)

    queue = await channel.declare_queue("user", durable=True)
    # Bind the queue to the exchange
    await queue.bind(exchange, "booking.user")

    await queue.consume(on_message)
    print("RabbitMQ consumer started")
    await asyncio.Future()  # Run forever


## AMQP items end ################################################################################################

## OLD SQL Alchemy Code ################################################################################################
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     "mysql+mysqlconnector://ticketboost:veryS3ecurePassword@mysql:3306/bolabola_user"
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# db = SQLAlchemy()
# db = db.init_app(app)
# db.app = app

##  Old Model Code
# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.String(120), primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     tickets = db.Column(db.JSON, nullable=True)
#     premium = db.Column(db.String(80), nullable=False)

#     def __init__(self, id, name, email, tickets, premium):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.tickets = tickets
#         self.premium = premium

#     def json(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "email": self.email,
#             "tickets": self.tickets,
#             "premium": self.premium,
#         }
## OLD SQL Alchemy Code end ################################################################################################


app = Quart(__name__)
DATABASE_URL = (
    "mysql+aiomysql://ticketboost:veryS3ecurePassword@mysql:3306/bolabola_user"
)

engine = create_async_engine(DATABASE_URL, echo=True)

# Create a base class for your models
Base = declarative_base()

# Configure Session class to use AsyncSession
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


class User(Base):
    __tablename__ = "user"
    id = Column(String(120), primary_key=True)
    name = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False)
    tickets = Column(JSON, nullable=True)
    premium = Column(String(80), nullable=False)

    def __init__(self, id, name, email, tickets, premium):
        self.id = id
        self.name = name
        self.email = email
        self.tickets = tickets
        self.premium = premium

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "tickets": self.tickets,
            "premium": self.premium,
        }


# path to test if the service is running
@app.route("/ping", methods=["GET"])
async def ping():
    print("pinged")
    return "pong"


############################################################################################################
#########################################    VIEW ALL USER INFO    #########################################
############################################################################################################
# path to print all users
@app.route("/", methods=["GET"])
async def home():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User))
            userlist = result.scalars().all()
            if len(userlist) == 0:
                return jsonify({"code": 404, "message": "No users found"})
            data = [user.json() for user in userlist]
            return jsonify({"code": 200, "data": data})


############################################################################################################
###############################    VIEW PARTICULAR USER INFO    ###########################################
############################################################################################################
# view particular user's info, given by user_id
@app.route("/<int:id>", methods=["GET"])
async def view_user(id):
    async with AsyncSessionLocal() as session:
        user = await session.get(User, str(id))
        if user is None:
            return jsonify({"code": 404, "message": "User not found"})
        return jsonify({"code": 200, "data": user.json()})


############################################################################################################
########################################    CREATE USER     ################################################
############################################################################################################
# path to check if user exists, and to create a new user if not.
@app.route("/check-create", methods=["POST"])
async def check_create_user():
    """
    This method creates a new user using the info received by Auth0.
    Sample payload:
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "user_id": "auth0|1234"
    }
    """
    data = await request.get_json()  # Asynchronously get the JSON data from the request
    if data is None:
        return jsonify({"code": 400, "message": "User info not provided"})

    received_user_id = data["user_id"]

    # Use an async session to interact with the database
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Asynchronously query for an existing user
            existing_user = await session.execute(
                select(User).filter_by(id=received_user_id)
            )
            user = existing_user.scalars().first()

            if user is not None:
                # If user exists, return an error message
                print("User already exists")
                return jsonify({"code": 400, "message": "User already exists"})

            # If user does not exist, create a new User instance
            new_user = User(
                id=received_user_id,
                name=data["name"],
                email=data["email"],
                tickets=None,
                premium="N",
            )

            # Add the new user to the session and commit the changes asynchronously
            session.add(new_user)
            await session.commit()
    print("User created successfully")
    return jsonify({"code": 201, "message": "User created successfully"})


############################################################################################################
##################################    VIEW USER TICKETS     ################################################
############################################################################################################
# view all tickets bought by the user
@app.route("/<int:id>/tickets", methods=["GET"])
async def view_all_user_tickets(id):
    """
    This method returns all the tickets owned by the user.
    Query will join the User and Ticket tables and return the tickets owned by the user.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, str(id))
            if user is None:
                return jsonify({"code": 404, "message": "User not found"})
            if user.tickets is None:
                return jsonify({"code": 404, "message": "User has no tickets"})
            return jsonify({"code": 200, "data": user.tickets})

# view a specific ticket bought by the user by serial number
@app.route("/<int:id>/tickets/<int:serial_no>", methods=["GET"])
async def view_ticket_by_serial_no(id, serial_no):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, str(id))
            if user is None:
                return jsonify({"code": 404, "message": "User not found"})
            if user.tickets is None:
                return jsonify({"code": 404, "message": "User has no tickets"})
            for ticket in user.tickets:
                if ticket["serial_no"] == str(serial_no):
                    return jsonify({"code": 200, "data": ticket})
            return jsonify({"code": 404, "message": "Ticket not found"})

# view a specific ticket bought by the user by match id
@app.route("/<int:id>/tickets/match/<int:match_id>", methods=["GET"])
async def view_ticket_by_match_id(id, match_id):
    """
    This method returns the details of a specific ticket owned by the user.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, str(id))
            if user is None:
                return jsonify({"code": 404, "message": "User not found"})
            if user.tickets is None:
                return jsonify({"code": 404, "message": "User has no tickets"})
            for ticket in user.tickets:
                if ticket["match_id"] == str(match_id):
                    return jsonify({"code": 200, "data": ticket})
            return jsonify({"code": 404, "message": "Ticket not found"})

############################################################################################################
#################################    END OF VIEW USER TICKETS    ###########################################
############################################################################################################


############################################################################################################
####################################    ADD A USER TICKET     ##############################################
############################################################################################################
# add a ticket to the user's list of tickets
@app.route("/<int:id>/tickets", methods=["POST"])
async def add_ticket_to_user(id):
    """
    This method adds a ticket to the user's list of tickets.
    Sample ticket:
    {
        "match_id": "1",
        "ticket_category": "A",
        "serial_no": "100"
    }
    """
    data = await request.get_json()
    if data is None:
        return jsonify({"code": 400, "message": "Ticket info not provided"})
    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.get(User, str(id))
            if user is None:
                return jsonify({"code": 404, "message": "User not found"})

            # check if the user already has the ticket
            if user.tickets is not None:
                for t in user.tickets:
                    if t["serial_no"] == data["serial_no"]:
                        return jsonify({"code": 400, "message": "User already has the ticket"})

            # add the ticket to the user's list of tickets
            if user.tickets is None:
                user.tickets = [data]
            else:
                user.tickets.append(data)

            # inform sqlalchemy that the tickets attribute has been modified. This MUST BE DONE because sqlalchemy got problem with JSON
            flag_modified(user, "tickets")

            await session.commit()
            return jsonify({"code": 201, "message": "Ticket added successfully"})

############################################################################################################
####################################    END OF ADD A USER TICKET     #######################################
############################################################################################################


############################################################################################################
####################################    DELETE A USER TICKET     ###########################################
############################################################################################################
# delete a ticket from the user's list of tickets using the payment intent
# this will be used when the user refunds a transaction successfully
# because each transaction can have multiple tickets, we have to look for the whole list of tickets
@app.route("/<int:id>/tickets", methods=["DELETE"])
async def delete_ticket_from_user(id):
    """
    This method deletes a ticket from the user's list of tickets.
    This will be used when the user refunds a ticket successfully.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            payment_intent = request.json.get("payment_intent")
            tickets_deleted = False
            user = await session.get(User, str(id))
            if user is None:
                return jsonify({"code": 404, "message": "User not found"})
            if user.tickets is None:
                return jsonify({"code": 404, "message": "User has no tickets"})
            for ticket in user.tickets: # there is a need to loop through all the tickets because there can be multiple tickets with the same payment_intent
                if ticket["payment_intent"] == payment_intent:
                    user.tickets.remove(ticket)
                    flag_modified(user, "tickets")
                    await session.commit()
                    tickets_deleted = True 
            if tickets_deleted:
                return jsonify({"code": 200, "message": "Ticket deleted successfully"})
            return jsonify({"code": 404, "message": "Ticket not found"})

############################################################################################################
####################################    END OF DELETE A USER TICKET     ####################################
############################################################################################################

if __name__ == "__main__":

    async def main():
        await asyncio.gather(
            app.run_task(host="0.0.0.0", port=9004, debug=False),  # Run Quart here
            amqp(),  # Run AMQP here
        )

    asyncio.run(main())
