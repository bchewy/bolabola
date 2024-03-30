import redis
from flask import Response
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import logging
import json
import quart_flask_patch
from quart import Quart, jsonify, request
from motor.motor_asyncio import AsyncIOMotorClient
import pika
import os
import json
from threading import Thread
from flask_cors import CORS
import asyncio
import aio_pika
import aioredis
import datetime
import aiocron


app = Quart(__name__)
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)
mongo_client = MongoClient("mongodb://mongodb:27017/")
app.config["MONGO_URI"] = "mongodb://mongodb:27017/"
engine = AsyncIOMotorClient(app.config["MONGO_URI"])  # using AsyncIOMotorClient
mongo_db = engine["tickets"]
tickets_collection = mongo_db["tickets"]
ticket_serial_counter = mongo_db["ticket_serial_counters"]
app.config["REDIS_URL"] = "redis://redis:6379/0"
redis_client = None  # Placeholder for the aioredis pool


async def init_redis_pool():
    global redis_client
    redis_client = aioredis.from_url(
        "redis://:verys3ruec@redis:6379/0", encoding="utf-8", decode_responses=True
    )
    print("REDIS Listener starting")


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
            print(f"User is removed from ticket {ticket_id}")
        print("All userids are removed from tickets")


# this code is adapted from /release endpoint
async def on_booking_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # delete ticket from redis
        print("Received message: ", message.body.decode())
        ticket_ids = json.loads(message.body.decode())["ticket_ids"]
        for ticket_id in ticket_ids.split(","):
            await delete_ticket(ticket_id)
            print(f"Ticket id {ticket_id} is removed from redis ")
        print("All tickets are removed from redis")

# on booking fail, remove user from ticket and delete ticket from redis
async def on_bookingFail_message(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Received message: {message.body.decode()}")
        ticket_ids = json.loads(message.body.decode())["ticket_ids"]
        # change string to list
        ticket_ids = ticket_ids.split(",")
        # remove user from ticket and delete ticket from redis
        for ticket_id in ticket_ids:
            await remove_user_from_ticket(ticket_id)
            print(f"User is removed from ticket {ticket_id}")
            await delete_ticket(ticket_id)
            print(f"Ticket id {ticket_id} is removed from redis ")
        print("All userids are removed from tickets")

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

    queueBookingFail = await channel.declare_queue("seat_fail", durable=True)
    await queueBookingFail.bind(exchangeBooking, "booking.seat_fail")
    await queueBookingFail.consume(on_bookingFail_message)

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
    available_tickets = tickets_collection.find(
        {"match_id": ObjectId(id), "user_id": None}
    )
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

        # Update ticket doc with reservation timestamp
        current_time = datetime.datetime.utcnow()
        await tickets_collection.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$set": {"reservation_timestamp": current_time}},
        )

        if await redis_client.set(f"ticket_hold:{ticket_id}", user_id, ex=180, nx=True):
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


# Counts the number of tickets for a particular match id.
@app.route("/tickets/count", methods=["POST"])
async def get_ticket_count():
    """
    Sample request:
    {
        "match_id": "5f9a6e6b3a9b1f2b8e7b4b1b"
    }
    """
    data = await request.json
    match_id = data["match_id"]

    # return the total number of tickets that do not have user_id on them
    total_tickets_available_A = 0
    total_tickets_available_B = 0
    total_tickets_available_C = 0
    # return the number of tickets that have been reserved
    total_tickets_reserved_A = 0
    total_tickets_reserved_B = 0
    total_tickets_reserved_C = 0

    # Retrieve all tickets related to the match_id from the database
    tickets = await tickets_collection.find({"match_id": ObjectId(match_id)}).to_list(
        length=None
    )

    print("TICKET VALUES", tickets)

    # loop through all the tickets in the database and count the number of tickets that do not have a user_id
    for ticket in tickets:
        if ticket["user_id"] is None:
            if str(ticket["category"]) == "A":
                total_tickets_available_A += 1
            elif str(ticket["category"]) == "B":
                total_tickets_available_B += 1
            elif str(ticket["category"]) == "C":
                total_tickets_available_C += 1

    # loop through all the tickets in the redis lock and count the number of tickets that have been reserved
    # get all tickets in redis
    tickets_in_redis = await redis_client.keys("ticket_hold:*")
    print("ALL TICKETS IN REDIS", tickets_in_redis)
    for redis_ticket in tickets_in_redis:
        redis_ticket = redis_ticket.split(":")[1]
        ticket = await tickets_collection.find_one({"_id": ObjectId(redis_ticket)})
        print("ONE of the TICKET IN REDIS", ticket)
        if str(ticket["match_id"]) == match_id:
            if str(ticket["category"]) == "A":
                total_tickets_reserved_A += 1
                total_tickets_available_A += 1
            elif str(ticket["category"]) == "B":
                total_tickets_reserved_B += 1
                total_tickets_available_B += 1
            elif str(ticket["category"]) == "C":
                total_tickets_reserved_C += 1
                total_tickets_available_C += 1

    # return the ticket_ids of all the tickets, in case someone needs it
    ticket_ids = [str(ticket["_id"]) for ticket in tickets]

    return (
        jsonify(
            {
                "match_id": match_id,
                "reserved_tickets": {
                    "A": total_tickets_reserved_A,
                    "B": total_tickets_reserved_B,
                    "C": total_tickets_reserved_C,
                },
                "available_tickets": {
                    "A": total_tickets_available_A,
                    "B": total_tickets_available_B,
                    "C": total_tickets_available_C,
                },
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


async def cleanup_expired_reservations():
    # Define the expiration time (e.g., 5 minutes)
    print("Running cleanup_expired_reservations")
    expiration_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=3)
    # Find tickets with an old reservation timestamp and no confirmed user_id
    expired_tickets = await tickets_collection.find(
        {
            "reservation_timestamp": {"$lt": expiration_time},
            "user_id": {"$exists": True},
        }
    ).to_list(None)
    # For each expired ticket, remove the reservation timestamp and release any Redis hold
    print("Expired tickets: ", expired_tickets)
    for ticket in expired_tickets:
        ticket_id = str(ticket["_id"])
        await tickets_collection.update_one(
            {"_id": ObjectId(ticket_id)},
            {"$unset": {"reservation_timestamp": "", "user_id": ""}},
        )
        # Attempt to release the Redis hold, if it still exists
        await redis_client.delete(f"ticket_hold:{ticket_id}")
        print("Completed cleanup")


# ================================ Seat Main END ============================================================================================================================================================================================================


# Health Check
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "alive"}), 200


@aiocron.crontab("*/3 * * * *")
async def scheduled_cleanup():
    await cleanup_expired_reservations()


if __name__ == "__main__":

    async def main():
        await init_redis_pool()  # Initialize Redis pool
        scheduled_cleanup.start()
        await asyncio.gather(
            app.run_task(port=9009, debug=True, host="0.0.0.0"),
            amqp(),  # Run AMQP here
        )

    asyncio.run(main())
