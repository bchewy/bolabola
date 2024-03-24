# from flask import Flask, request, jsonify
import redis
from flask import Response
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import logging
import json

import quart_flask_patch
from quart import Quart, jsonify, request

# from quart_motor import Motor
from motor.motor_asyncio import AsyncIOMotorClient

# Others
import pika
import os
import json
from threading import Thread
from flask_cors import CORS
import asyncio
import aio_pika


app = Quart(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

# MongoDB setup
mongo_client = MongoClient("mongodb://mongodb:27017/")
app.config["MONGO_URI"] = "mongodb://mongodb:27017/"
engine = AsyncIOMotorClient(app.config["MONGO_URI"])  # using AsyncIOMotorClient
mongo_db = engine["tickets"]
tickets_collection = mongo_db["tickets"]

# Ticket Serial Counter Collection
ticket_serial_counter = mongo_db["ticket_serial_counters"]

# Redis setup
app.config["REDIS_URL"] = "redis://redis:6379/0"
redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])


# ==== Ticket Counter MONGO Functions ====
async def get_next_ticket_serial():
    serial_counter = await ticket_serial_counter.find_one_and_update(
        {"_id": "ticket_serial"},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
    )
    return serial_counter["seq"]


async def create_ticket_for_user(user_id, match_id, ticket_category):
    # Get the next serial number
    serial_no = await get_next_ticket_serial()

    # Create a new ticket document
    new_ticket = {
        "serial_no": serial_no,
        "match_id": match_id,
        "ticket_category": ticket_category,
        "user_id": user_id,
        # Add other necessary fields
    }

    # Insert the new ticket into the tickets collection
    await tickets_collection.insert_one(new_ticket)

    # Update the user's document in the users collection with the new ticket's serial number
    await mongo_db["users"].update_one(
        {"_id": user_id}, {"$push": {"tickets": serial_no}}
    )

    return new_ticket


# ==== AMQP Functions ====


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        # to insert the message into the database


async def amqp():
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        "booking", aio_pika.ExchangeType.DIRECT, durable=True
    )
    queue = await channel.declare_queue("seat", durable=True)
    await queue.bind(exchange, "booking.seat")
    await queue.consume(on_message)
    print("RabbitMQ consumer started")
    await asyncio.Future()  # Run forever


# ==== AMQP Functions end ====


# ================================ Helper Main Functons ============================================================================================================================================================================================================


@app.route("/availabletickets/<id>", methods=["GET"])
async def get_available_tickets(id):
    # match_id = request.args.get('id')
    available_tickets = tickets_collection.find({"match_id": id, "user_id": None})
    tickets_list = []
    async for ticket in available_tickets:
        tickets_list.append(
            {
                # add serial number as auto increment ID for the ticket - mongoDB
                "serial_no": ticket["serial_no"],
                "match_id": ticket["match_id"],
                "ticket_category": ticket["ticket_category"],
                "seat_number": ticket["seat_number"],
                "user_id": ticket["user_id"] if ticket["user_id"] else "None",
                "ticket_id": str(ticket["_id"]),
            }
        )
    return jsonify(tickets_list), 200


# ================================ Seat Main Functons ============================================================================================================================================================================================================


@app.route("/reserve", methods=["POST"])
def reserve_seat():
    print("Reserve seat called")
    data = request.json
    user_id = data["user_id"]
    match_id = data["match_id"]
    ticket_category = data["ticket_category"]
    # Check if user_id already has a seat reserved for this match
    existing_ticket = tickets_collection.find_one(
        {"match_id": match_id, "user_id": user_id}
    )
    if existing_ticket:
        return (
            jsonify({"error": "User already has a seat reserved for this match"}),
            409,
        )

    # Find an available ticket for the given match and category
    ticket = tickets_collection.find_one_and_update(
        {
            "match_id": match_id,
            "ticket_category": ticket_category,
            "user_id": None,
        },
        {"$set": {"user_id": user_id}},
        return_document=ReturnDocument.AFTER,
    )

    if ticket:
        if redis_client.set(  # ticket_id has to change to serial_no
            f"ticket_hold:{match_id}:{ticket_category}:{ticket['_id']}",
            user_id,
            ex=300,
            nx=True,
        ):
            return (
                jsonify(
                    {
                        "message": "Seat reserved",
                        "match_id": match_id,
                        "ticket_category": ticket_category,
                        "ticket_id": str(ticket["_id"]),
                    }
                ),
                200,
            )
        else:
            tickets_collection.update_one(
                {"_id": ticket["_id"]}, {"$unset": {"user_id": ""}}
            )
            return jsonify({"error": "Seat is currently on hold"}), 409
    else:
        return (
            jsonify({"error": "No available tickets for this match and category"}),
            400,
        )


@app.route("/release", methods=["POST"])
def release_seat():
    data = request.json
    serial_no = data["serial_no"]
    redis_client.delete(f"ticket_hold:{serial_no}")
    tickets_collection.update_one({"serial_no": serial_no}, {"$unset": {"user_id": ""}})
    return jsonify({"message": "Seat released", "serial_no": serial_no}), 200


@app.route("/validate_reservation/", methods=["POST"])
def validate_reservation():
    data = request.json
    serial_no = data["serial_no"]
    ticket = tickets_collection.find_one({"serial_no": serial_no})
    if ticket and "user_id" in ticket:
        is_held = redis_client.exists(f"ticket_hold:{serial_no}")
        if is_held:
            return (
                jsonify(
                    {
                        "status": "reserved",
                        "message": "This seat is currently on hold.",
                        "user_id": ticket["user_id"],
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "status": "confirmed",
                        "message": "This seat has been confirmed by a user.",
                        "user_id": ticket["user_id"],
                    }
                ),
                200,
            )
    elif ticket:
        return (
            jsonify({"status": "available", "message": "This seat is available."}),
            200,
        )
    else:
        return jsonify({"error": "Seat not found"}), 404


# ================================ Seat Main END ============================================================================================================================================================================================================


# Health Check
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200


if __name__ == "__main__":

    async def main():
        await asyncio.gather(
            app.run_task(port=9009, debug=True, host="0.0.0.0"),
            amqp(),  # Run AMQP here
        )

    asyncio.run(main())
