DROP DATABASE IF EXISTS bolabola_user;
CREATE DATABASE bolabola_user;
USE bolabola_user;

-- Create the User table
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    stripe_id VARCHAR(120) UNIQUE,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    tickets JSON
);

-- Insert dummy data for users
INSERT INTO User (id, name, email, stripe_id, username, password, tickets) VALUES
    (1, 'John Doe', 'johndoe@gmail.com', '123', 'johndoe', 'johndoe', '[{"match_id": 123, "ticket_category": "A", "serial_no": "1"}, {"match_id": 456, "ticket_category": "A", "serial_no": "2"}]'),
    (2, 'Alice Smith', 'alice@example.com', '456', 'alicesmith', 'alicesmith', '[{"match_id": 1, "ticket_category": "A", "serial_no": "3"}, {"match_id": 2, "ticket_category": "B", "serial_no": "4"}]'),
    (3, 'Bob Johnson', 'bob@example.com', '789', 'bobjohnson', 'bobjohnson', '[{"match_id": 3, "ticket_category": "C", "serial_no": "5"}, {"match_id": 4, "ticket_category": "A", "serial_no": "6"}]'),
    (4, 'Eve Brown', 'eve@example.com', '101', 'evebrown', 'evebrown', '[{"match_id": 5, "ticket_category": "A", "serial_no": "7"}, {"match_id": 1, "ticket_category": "B", "serial_no": "8"}]'),
    (5, 'Charlie Wilson', 'charlie@example.com', '112', 'charliewilson', 'charliewilson', '[{"match_id": 2, "ticket_category": "C", "serial_no": "9"}, {"match_id": 3, "ticket_category": "A", "serial_no": "10"}]'),
    (6, 'Grace Lee', 'grace@example.com', '113', 'gracelee', 'gracelee', '[{"match_id": 4, "ticket_category": "B", "serial_no": "11"}, {"match_id": 5, "ticket_category": "A", "serial_no": "12"}]'),
    (7, 'David Martinez', 'david@example.com', '114', 'davidmartinez', 'davidmartinez', '[{"match_id": 1, "ticket_category": "A", "serial_no": "13"}, {"match_id": 2, "ticket_category": "C", "serial_no": "14"}]'),
    (8, 'Emma Rodriguez', 'emma@example.com', '115', 'emmarodriguez', 'emmarodriguez', '[{"match_id": 3, "ticket_category": "B", "serial_no": "15"}, {"match_id": 4, "ticket_category": "A", "serial_no": "16"}]'),
    (9, 'Jack Wilson', 'jack@example.com', '116', 'jackwilson', 'jackwilson', '[{"match_id": 5, "ticket_category": "C", "serial_no": "17"}, {"match_id": 1, "ticket_category": "A", "serial_no": "18"}]'),
    (10, 'Sophia Anderson', 'sophia@example.com', '117', 'sophiaanderson', 'sophiaanderson', '[{"match_id": 2, "ticket_category": "B", "serial_no": "19"}, {"match_id": 3, "ticket_category": "A", "serial_no": "20"}]'),
    (11, 'William Taylor', 'william@example.com', '118', 'williamtaylor', 'williamtaylor', '[{"match_id": 4, "ticket_category": "C", "serial_no": "21"}, {"match_id": 5, "ticket_category": "A", "serial_no": "22"}]'),
    (12, 'Olivia Martin', 'olivia@example.com', '119', 'oliviamartin', 'oliviamartin', '[{"match_id": 1, "ticket_category": "B", "serial_no": "23"}, {"match_id": 2, "ticket_category": "A", "serial_no": "24"}]'),
    (13, 'Liam Lewis', 'liam@example.com', '120', 'liamlewis', 'liamlewis', '[{"match_id": 3, "ticket_category": "C", "serial_no": "25"}, {"match_id": 4, "ticket_category": "A", "serial_no": "26"}]'),
    (14, 'Charlotte Garcia', 'charlotte@example.com', '121', 'charlottegarcia', 'charlottegarcia', '[{"match_id": 5, "ticket_category": "B", "serial_no": "27"}, {"match_id": 1, "ticket_category": "A", "serial_no": "28"}]'),
    (15, 'Noah Rodriguez', 'noah@example.com', '122', 'noahrodriguez', 'noahrodriguez', '[{"match_id": 2, "ticket_category": "C", "serial_no": "29"}, {"match_id": 3, "ticket_category": "A", "serial_no": "30"}]'),
    (16, 'Sophie Johnson', 'sophie@example.com', 'sophiejohnson', 'sophiejohnson'),
    (17, 'James Williams', 'james@example.com', 'jameswilliams', 'jameswilliams'),
    (18, 'Ava Brown', 'ava@example.com', 'avabrown', 'avabrown'),
    (19, 'Michael Jones', 'michael@example.com', 'michaeljones', 'michaeljones'),
    (20, 'Emily Martinez', 'emily@example.com', 'emilymartinez', 'emilymartinez');
