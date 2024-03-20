SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `bolabola_user` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bolabola_user`;

-- Create the user table
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
    `id` VARCHAR(120) PRIMARY KEY,
    `name` VARCHAR(80) NOT NULL,
    `email` VARCHAR(120) UNIQUE NOT NULL,
    `tickets` JSON,
    `premium` VARCHAR (10) DEFAULT 'N'
) ENGINE=InnoDB;

-- Insert dummy data for users
INSERT INTO `user` (`id`, `name`, `email`, `tickets`, `premium`) VALUES
    ("1", 'John Doe', 'johndoe@gmail.com', '[{"match_id": "123", "ticket_category": "A", "serial_no": "1"}, {"match_id": "456", "ticket_category": "A", "serial_no": "2"}]', 'Y'),
    ("2", 'Alice Smith', 'alice@example.com', '[{"match_id": "1", "ticket_category": "A", "serial_no": "3"}, {"match_id": "2", "ticket_category": "B", "serial_no": "4"}]', 'N'),
    ("3", 'Bob Johnson', 'bob@example.com', '[{"match_id": "3", "ticket_category": "C", "serial_no": "5"}, {"match_id": "4", "ticket_category": "A", "serial_no": "6"}]', 'N');

-- Grant access to the user
-- CREATE USER 'ticketboost'@'%' IDENTIFIED BY 'ticketboost';
GRANT CREATE, ALTER, INDEX, LOCK TABLES, REFERENCES, UPDATE, DELETE, DROP, SELECT, INSERT ON `bolabola_user`.* TO 'ticketboost'@'%';

-- Flush privileges
FLUSH PRIVILEGES;
