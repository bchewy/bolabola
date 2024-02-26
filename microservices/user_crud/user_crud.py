import os
import user_schemas, ticket_schemas
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import requests
from user_schemas import *

AUTH_ENDPOINT = os.environ.get('AUTH_ENDPOINT') # to create this endpoint in the future
STRIPE_ENDPOINT = os.environ.get('STRIPE_ENDPOINT') # to create this endpoint in the future

# get user from the database
def get_user(email: str) -> user_schemas.UserAccount:
    """
    Get a user from the database
    """
    user_response = requests.get(f"{AUTH_ENDPOINT}/getUser/{email}")

    if user_response.status_code != 200:
        raise Exception("User not found")
    
    user_json = user_response.json()
    return user_schemas.UserAccount(
        id=user_json['id'],
        name=user_json['name'],
        email=user_json['email'],
        username=user_json['username'],
        created_at=datetime.strptime(user_json['created_at'], '%Y-%m-%d %H:%M:%S.%f'),
        updated_at=datetime.strptime(user_json['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
    )

# get all tickets from database
def get_all_tickets(user_id: int) -> ticket_schemas.TicketOwned:
    tickets_response = requests.get(f"/users/{user_id}/tickets")

    if tickets_response.status_code != 200:
        raise Exception("Failed to fetch tickets")

    tickets_json = tickets_response.json()
    tickets = []
    for ticket_data in tickets_json:
        ticket = ticket_schemas.TicketOwned(
            event_id=ticket_data['event_id'],
            venue_id=ticket_data['venue_id'],
            seat_id=ticket_data['seat_id'],
            user_id=ticket_data['user_id'],
            purchased_at=datetime.strptime(ticket_data['purchased_at'], '%Y-%m-%d %H:%M:%S.%f')
        )
        tickets.append(ticket)

    return tickets

# get ticket from database
def get_ticket(user_id: int, ticket_id: int) -> ticket_schemas.TicketOwned:
    """
    Get a specific ticket from the database by ticket ID
    """
    ticket_response = requests.get(f"/users/{user_id}/tickets/{ticket_id}")

    if ticket_response.status_code != 200:
        raise Exception("Failed to fetch ticket")

    ticket_json = ticket_response.json()

    return ticket_schemas.TicketOwned(
        event_id=ticket_json['event_id'],
        venue_id=ticket_json['venue_id'],
        seat_id=ticket_json['seat_id'],
        user_id=ticket_json['user_id'],
        purchased_at=datetime.strptime(ticket_json['purchased_at'], '%Y-%m-%d %H:%M:%S.%f')
    )

# delete ticket from database
def delete_ticket(ticket_id: int):
    """
    Delete a ticket by its ID
    """
    # Retrieve the ticket from the database
    ticket = ticket_schemas.TicketModel.query.get(ticket_id)

    if ticket:
        # If the ticket exists, delete it from the database
        db.session.delete(ticket)
        db.session.commit()
    else:
        # If the ticket doesn't exist, raise an exception
        raise Exception(f"Ticket with ID {ticket_id} not found")