CREATE DATABASE IF NOT EXISTS `event_mgt` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event_mgt`;

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
   `event_id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `description` VARCHAR(100) NOT NULL,
    `start_date` DATETIME NOT NULL,
    `location` VARCHAR(100) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO events (name, description, start_date, location)
VALUES ('Rock Festival', 'Annual rock festival featuring top bands', '2024-06-05 20:00:00', 'Arena'),
       ('Jazz Night', 'Live jazz performance by world-renowned musicians', '2024-04-25 19:30:00', 'Opera House'),
       ('Pop Concert', 'Pop music extravaganza with chart-topping artists', '2025-01-20 18:00:00', 'Stadium'),
       ('Classical Symphony', 'Orchestral performance of classical symphonies', '2025-04-15 19:00:00', 'Concert Hall'),
       ('Indie Showcase', 'Showcase of indie bands and emerging artists', '2024-08-10 20:30:00', 'Music Club'),
       ('Electronic Dance Party', 'EDM party featuring top DJs and electronic artists', '2025-07-08 22:00:00', 'Nightclub'),
       ('Country Music Fest', 'Celebration of country music with live performances', '2024-09-22 17:00:00', 'Fairground'),
       ('Hip-Hop Extravaganza', 'Hip-hop concert with iconic rap artists and DJs', '2025-03-18 21:00:00', 'Hip-Hop Venue'),
       ('Reggae Jam', 'Reggae music festival with live bands and DJs', '2024-10-05 19:30:00', 'Beachfront'),
       ('Latin Fiesta', 'Fiesta featuring Latin music, dance, and culture', '2025-08-20 18:30:00', 'Cultural Center'),
       ('Blues Revival', 'Revival of blues music with legendary blues artists', '2024-11-30 20:00:00', 'Blues Club'),
       ('Metal Madness', 'Metal music festival with headbanging bands and mosh pits', '2025-06-15 21:00:00', 'Outdoor Arena'),
       ('Acoustic Serenade', 'Intimate acoustic concert with singer-songwriters', '2024-12-20 19:00:00', 'Coffeehouse'),
       ('R&B Soul Spectacular', 'Spectacular R&B and soul concert with iconic performers', '2025-02-10 20:30:00', 'Soul Lounge'),
       ('Folk Festival', 'Folk music festival featuring traditional and contemporary folk artists', '2024-07-20 18:00:00', 'Park Amphitheater'),
       ('Gospel Celebration', 'Gospel music celebration with uplifting performances', '2025-05-10 19:30:00', 'Church'),
       ('World Music Gala', 'Gala showcasing diverse world music and cultural performances', '2024-03-15 19:00:00', 'Cultural Center'),
       ('Punk Rock Riot', 'Punk rock concert featuring high-energy bands and mosh pits', '2025-09-10 20:00:00', 'Club Basement'),
       ('Funk Fusion', 'Funky fusion concert blending funk, jazz, and soul', '2024-02-15 21:00:00', 'Music Hall'),
       ('Ska Skank', 'Ska music extravaganza with ska bands and skanking dance', '2025-10-20 19:30:00', 'Skate Park');



-- Path: event_mgt/event_mgt.sql
