const Redis = require('ioredis');
const redis = new Redis(); // Connects to 127.0.0.1:6379

const ticketKey = "event:123:ticket:456"; // Example ticket key for Redis

// Function to simulate holding a ticket
async function holdTicket(ticketId, holdDuration) {
    const result = await redis.setex(ticketKey, holdDuration, "held");
    console.log(`Ticket ${ticketId} is now held for ${holdDuration} seconds.`);
    return result;
}

// Function to check ticket status
async function checkTicketStatus(ticketId) {
    const status = await redis.get(ticketKey);
    console.log(`Ticket ${ticketId} status: ${status}`);
}

// Simulate releasing the ticket if not purchased within 10 minutes (600 seconds)
holdTicket("456", 600).then(() => {
    setTimeout(() => {
        checkTicketStatus("456");
    }, 600 * 1000); // Check status after 10 minutes
});
