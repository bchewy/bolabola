import redis
import time

# Connect to Redis container
r = redis.Redis(host='localhost', port=6379, db=0)

# Function to hold a ticket
def hold_ticket(ticket_id, user_id, ttl=10):
    """
    Hold a ticket for a user with a TTL.
    :param ticket_id: ID of the ticket to hold.
    :param user_id: ID of the user holding the ticket.
    :param ttl: Time to live in seconds. Default is 600 seconds (10 minutes).
    """
    r.setex(f"ticket:{ticket_id}", ttl, user_id)
    print(f"Ticket {ticket_id} is now held for user {user_id} for {ttl} seconds.")

def does_ticket_exist(ticket_id):
    """
    Check if a ticket exists.
    :param ticket_id: ID of the ticket to check.
    :return: True if the ticket exists, False otherwise.
    """
    return r.exists(f"ticket:{ticket_id}")


# Hold a ticket
hold_ticket('12345', 'user_1')

time.sleep(5)
print("Ticket exist? 5ms mark",does_ticket_exist('12345'))


time.sleep(15) 
print("Ticket exist? 20ms mark",does_ticket_exist('12345'))



