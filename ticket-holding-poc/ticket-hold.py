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

# Example usage
hold_ticket('12345', 'user_1')

# Optional: Check if the ticket is still held after 10 minutes
print('''r.exists(f"ticket:12345")''', r.exists(f"ticket:12345"))
time.sleep(15) # Wait for 10 minutes
if r.exists(f"ticket:12345"):
    print("Ticket is still held.")
else:
    print("Ticket hold has expired.")
