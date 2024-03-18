# User Profile Microservice
- main.py acts as the entry point for the user microservice.
- user_schemas is the pydantic models for the user_crud microservice and db.

The User Database will be in SQL and has 1 table:
- User Table

Sample User:
```
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
    "stripe_id": "123",
    "username": "johndoe",
    "password": "johndoe",
    "tickets": [
        {"match_id": 123, "ticket_category": "A", "serial_no": "1", "payment_intent": "abc"},
        {"match_id": 456, "ticket_category": "A", "serial_no": "2", "payment_intent": "cbd"},
    ]
}
```
note that stripe_id is optional and is only present if the user has bought a ticket.

![user db schema](schema.png)


If you get this error in mysql:
`--initialize specified but the data directory has files in it. Aborting...`
Delete the `dbdata` folder and compose up again.

## To implement
- [ ] Track the logged in user
- [ ] If user is not registered, create a new user
- [ ] RabbitMQ is not working
- [ ] Create a lot of payment intents and put into the user database. 

## Issues
- [ ] If your user gets JSON format error, use docker compose up --force-recreate mysql

------

archived sql init
```sql

------------------------------------------------------------ to change the data to show real stripe_id and real tickets
-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- SET time_zone = "+00:00";

-- CREATE DATABASE IF NOT EXISTS `bolabola_user` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- USE `bolabola_user`;

-- -- Create the user table
-- DROP TABLE IF EXISTS `user`;
-- CREATE TABLE IF NOT EXISTS `user` (
--     `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
--     `name` VARCHAR(80) NOT NULL,
--     `email` VARCHAR(120) UNIQUE NOT NULL,
--     `stripe_id` VARCHAR(120) UNIQUE,
--     `username` VARCHAR(80) UNIQUE NOT NULL,
--     `password` VARCHAR(120) NOT NULL,
--     `tickets` JSON,
--     `premium` ENUM('Y', 'N') DEFAULT 'N'
-- ) ENGINE=InnoDB;

-- -- Insert dummy data for users
-- INSERT INTO `user` (`id`, `name`, `email`, `stripe_id`, `username`, `password`, `tickets`, `premium`) VALUES
--     (1, 'Eating Haaland', 'eh@example.com', 'cus_PkkXbmLwML0CQ5', 'eatinghaaland', 'eatinghaaland', '[{"match_id": "123", "ticket_category": "A", "serial_no": "1", "payment_intent": ""}, {"match_id": "456", "ticket_category": "A", "serial_no": "2", "payment_intent": ""}]', 'Y'),
--     (2, 'No Salad', 'ns@example.com', 'cus_PkkXYdrr1OJ5VQ', 'nosalad', 'nosalad', '[{"match_id": "2", "ticket_category": "B", "serial_no": "4", "payment_intent": ""}]', 'N'),
--     (3, 'Wayne Macarooney', 'wm@example.com', 'cus_PkkYXUkcZxDF0t', 'waynemacarooney', 'waynemacarooney', '[{"match_id": "3", "ticket_category": "C", "serial_no": "5"}, {"match_id": "4", "ticket_category": "A", "serial_no": "6"}]', 'N'),

-- -- Grant access to the user
-- CREATE USER 'ticketboost'@'%' IDENTIFIED BY 'ticketboost';
-- GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `bolabola_user`.* TO 'ticketboost'@'%';

-- -- Flush privileges
-- FLUSH PRIVILEGES;
```