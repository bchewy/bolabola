DROP DATABASE IF EXISTS ticketboost_ticket;
CREATE DATABASE ticketboost_ticket;
USE ticketboost_ticket;

CREATE TABLE Ticket (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER,
    event_id INTEGER NOT NULL,
    venue_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- INSERT INTO Ticket(id, user_id, event_id, seat_id, purchased_at) 
-- VALUES
