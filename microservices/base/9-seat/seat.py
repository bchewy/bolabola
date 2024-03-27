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
import aioredis


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
# redis_client = redis.StrictRedis.from_url(app.config["REDIS_URL"])
redis_client = None  # Placeholder for the aioredis pool


async def init_redis_pool():
    global redis_client
    redis_client = aioredis.from_url(
        "redis://:verys3ruec@redis:6379/0", encoding="utf-8", decode_responses=True
    )
    print("REDIS Listener starting")


# ==== Ticket Counter MONGO Functions ====
# async def get_next_ticket_serial():
#     serial_counter = await ticket_serial_counter.find_one_and_update(
#         {"_id": "ticket_serial"},
#         {"$inc": {"seq": 1}},
#         return_document=ReturnDocument.AFTER,
#     )
#     return serial_counter["seq"]


# async def create_ticket_for_user(user_id, match_id, ticket_category):
#     # Get the next serial number
#     serial_no = await get_next_ticket_serial()

#     # Create a new ticket document
#     new_ticket = {
#         "serial_no": serial_no,
#         "match_id": match_id,
#         "ticket_category": ticket_category,
#         "user_id": user_id,
#         # Add other necessary fields
#     }

#     # Insert the new ticket into the tickets collection
#     await tickets_collection.insert_one(new_ticket)

#     # Update the user's document in the users collection with the new ticket's serial number
#     await mongo_db["users"].update_one(
#         {"_id": user_id}, {"$push": {"tickets": serial_no}}
#     )

#     return new_ticket


# ==== AMQP Functions ====
async def on_refund_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        ticket_ids = json.loads(message.body.decode())["ticket_ids"]
        # change string to list
        ticket_ids = ticket_ids.split(",")
        # remove user from ticket and delete ticket from redis
        for ticket_id in ticket_ids:
            await remove_user_from_ticket(ticket_id)
            print(f"Ticket id {ticket_id} is removed from redis ")
        print("All tickets are removed from redis")


# this code is adapted from /release endpoint
async def on_booking_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # delete ticket from redis
        print("Received message: ", message.body.decode())
        ticket_ids = json.loads(message.body.decode())["ticket_ids"]
        for ticket_id in ticket_ids:
            await delete_ticket(ticket_id)
            print(f"Ticket id {ticket_id} is removed from redis ")
        print("All tickets are removed from redis")


async def delete_ticket(ticket_id):
    # Check if ticket_id is valid
    ticket_exists = await tickets_collection.count_documents(
        {"_id": ObjectId(ticket_id)}
    )
    if ticket_exists:
        # Only run redis_client.delete if ticket_hold exists
        ticket_hold_exists = await redis_client.exists(f"ticket_hold:{ticket_id}")
        if ticket_hold_exists:
            await redis_client.delete(f"ticket_hold:{ticket_id}")
        return json.dumps({"message": "Seat released", "ticket_id": ticket_id}), 200
    else:
        return json.dumps({"error": "Invalid ticket_id"}), 400


async def amqp():
    rabbitmq_url = "amqp://ticketboost:veryS3ecureP@ssword@rabbitmq/"
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()
    exchangeBooking = await channel.declare_exchange(
        "booking", aio_pika.ExchangeType.DIRECT, durable=True
    )
    queueBooking = await channel.declare_queue("seat", durable=True)
    await queueBooking.bind(exchangeBooking, "booking.seat")
    await queueBooking.consume(on_booking_message)

    exchangeRefunds = await channel.declare_exchange(
        "refunds", aio_pika.ExchangeType.DIRECT, durable=True
    )
    queueRefunds = await channel.declare_queue("seat", durable=True)
    await queueRefunds.bind(exchangeRefunds, "refunds.seat")
    await queueRefunds.consume(on_refund_message)
    
    print("RabbitMQ consumer started")
    await asyncio.Future()  # Run forever


# ==== AMQP Functions end ====


# ================================ Helper Main Functons ============================================================================================================================================================================================================


@app.route("/availabletickets/<id>", methods=["GET"])
async def get_available_tickets(id):
    # match_id = request.args.get('id')
    available_tickets = tickets_collection.find({"match_id": ObjectId(id), "user_id": None})
    print(available_tickets)
    tickets_list = []
    async for ticket in available_tickets:
        tickets_list.append(
            {
                # "serial_no": ticket["serial_no"],
                "ticket_id": str(ticket["_id"]),
                "user_id": ticket["user_id"] if ticket["user_id"] else "None",
                "match_id": str(ticket["match_id"]),
                "category": ticket["category"],
                "seat_number": ticket["seat_number"],
            }
        )
    return jsonify(tickets_list), 200
 

# ================================ Seat Main Functons ============================================================================================================================================================================================================


@app.route("/reserve", methods=["POST"])
async def reserve_seat():
    # Expects:
    # "userid", "match_id", "category", "quantity"
    data = await request.json
    required_fields = ["user_id", "match_id", "category", "quantity"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field(s)."}), 400

    print("Reserve seat called")
    user_id = data["user_id"]
    match_id = data["match_id"]
    category = data["category"]
    quantity = data["quantity"]

    # Print out debug items, userid, match_id, ticket_category
    print("User ID: ", user_id)
    print("Match ID: ", match_id)
    print("Ticket Category: ", category)
    print("Quantity of seats: ", quantity)

    # Check if user_id already has a seat reserved for this match
    # existing_ticket = await tickets_collection.find_one(
    #     {"match_id": match_id, "user_id": user_id}
    # )

    # Look for available tickets for this user for this match_id
    available_tickets = await tickets_collection.find(
        {"match_id": ObjectId(match_id), "user_id": None, "category": category}
    ).to_list(length=quantity)

    print("Printing out available tickets here: ", available_tickets)

    if available_tickets:
        print(f"Available ticket: {available_tickets} exists for user {user_id}")
    else:
        print("Not available tickets found ")

    # this list only contains reserved tickets for the user
    reserved_tickets = []
    for ticket in available_tickets:
        print("Ticket: ", ticket)
        ticket_id = str(ticket["_id"])
        print(f"Attempting to reserve ticket in Redis for ticket_id: {ticket_id}")
        if await redis_client.set(f"ticket_hold:{ticket_id}", user_id, ex=300, nx=True):
            print(f"Successfully reserved ticket in Redis for ticket_id: {ticket_id}")
            print("Reserved ticket: ", ticket_id)

            reserved_tickets.append(ticket_id)
        else:
            # Rollback logic here
            print("ERROR: Redis command did not work.")
            break

    if len(reserved_tickets) == quantity:
        print("Reserved tickets: ", reserved_tickets)
        print("Quantity: ", quantity)
        # Confirm the reservation in MongoDB
        for ticket_id in reserved_tickets:
            print("ticket_id: ", ticket_id)
            await tickets_collection.update_one(
                {"_id": ObjectId(ticket_id)}, {"$set": {"user_id": user_id}}
            )
        return (
            jsonify({"message": "Seats reserved", "ticket_ids": reserved_tickets}),
            200,
        )
    else:
        # Rollback in Redis
        for ticket_id in reserved_tickets:
            await redis_client.delete(f"ticket_hold:{ticket_id}")
        return (
            jsonify({"error": "Error: One or more seats are currently on hold/issues"}),
            409,
        )


# @app.route("/release", methods=["POST"])
async def release_seat(ticket_id):
    # Check if ticket_id is valid
    ticket_exists = await tickets_collection.count_documents(
        {"_id": ObjectId(ticket_id)}
    )
    if ticket_exists:
        # Only run redis_client.delete if ticket_hold exists
        ticket_hold_exists = await redis_client.exists(f"ticket_hold:{ticket_id}")
        if ticket_hold_exists:
            await redis_client.delete(f"ticket_hold:{ticket_id}")
        return jsonify({"message": "Seat released", "ticket_id": ticket_id}), 200
    else:
        return jsonify({"error": "Invalid ticket_id"}), 400


@app.route("/validate_reservation/", methods=["POST"])
async def validate_reservation():
    data = await request.json
    ticket_id = data["ticket_id"]
    user_id = data["user_id"]
    ticket = await tickets_collection.find_one({"_id": ObjectId(ticket_id)})
    if ticket and ticket.get("user_id") == user_id:
        return (
            jsonify(
                {
                    "status": "confirmed",
                    "message": "This seat has been confirmed by the user.",
                    "user_id": user_id,
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


# Counts the number of reserved tickets for a particular match id.
@app.route("/tickets/count", methods=["POST"])
async def get_ticket_count():
    data = await request.json

    if "match_id" not in data or "reserved" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    match_id = data["match_id"]
    reserved = data["reserved"]
    # Retrieve all tickets related to the match_id from the database
    tickets = await tickets_collection.find({"match_id": ObjectId(match_id)}).to_list(
        length=None
    )

    print("TICKET VALUES", tickets)
    ticket_ids = [
        str(ticket["_id"]) for ticket in tickets
    ]  # this contains ALL the tickets,

    if reserved:
        # Use a separate list to store tickets that are confirmed to be on hold
        confirmed_on_hold_tickets = []
        for t in ticket_ids:
            if await redis_client.exists(f"ticket_hold:{t}"):
                print(
                    "Adding ticket of ticket_id:{} into the confirmed_on_hold_tickets list".format(
                        t
                    )
                )
                confirmed_on_hold_tickets.append(t)
        ticket_ids = confirmed_on_hold_tickets  # Replace the original list with the filtered list
        ticket_count = len(ticket_ids)
    else:
        # Count tickets that are reserved (i.e., those with a non-empty "user_id" field)
        ticket_count = await tickets_collection.count_documents(
            {"match_id": ObjectId(match_id), "user_id": {"$ne": None}}
        )

    return (
        jsonify(
            {
                "match_id": match_id,
                "ticket_count": ticket_count,
                "ticket_ids": ticket_ids,  # will return all ticket_ids regardless
            }
        ),
        200,
    )


async def remove_user_from_ticket(ticket_id):
    # Find the ticket by its ID
    ticket = await tickets_collection.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        return json.dumps({"error": "Ticket not found"}), 404
    # Update the ticket to remove the user_id
    result = await tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)}, {"$set": {"user_id": None}}
    )
    if result.modified_count:
        return json.dumps({"message": "User removed from ticket successfully"}), 200
    else:
        return json.dumps({"error": "Failed to remove user from ticket"}), 500


# ================================ Seat Main END ============================================================================================================================================================================================================


# Health Check
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200


if __name__ == "__main__":

    async def main():
        await init_redis_pool()  # Initialize Redis pool
        await asyncio.gather(
            app.run_task(port=9009, debug=True, host="0.0.0.0"),
            amqp(),  # Run AMQP here
        )

    asyncio.run(main())
