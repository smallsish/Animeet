DROP TABLE IF EXISTS `event`;

CREATE TABLE `event` (
    `event_id` int NOT NULL AUTO_INCREMENT,
    `event_name` varchar(64) NOT NULL,
    `venue` varchar(64) NOT NULL,
    `entry_fee` float NOT NULL,
    `description` varchar(64) NOT NULL,
    `capacity` int NOT NULL,
    `slots_left` int NOT NULL,
    `time` timestamp NOT NULL,
    PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `event` 
(`event_id`, `event_name`, `venue`, `entry_fee`, `description`, `capacity`, `slots_left`, `time`) 
VALUES 
(1, 'Music Concert', 'City Hall', 50, 'An evening of classical music with a live orchestra.', 50, 45, '2024-12-25 19:00:00'), (2, 'Cosplayers Unite', 'Labrador Park', 20, 'Cosplay gathering.', 50, 49, '2024-12-25 19:00:00'), (3, 'Demon Slayer Movie Night', 'Changi Airport', 10, 'A relaxing evening for everyone to watch Demon Slayer.', 50, 50, '2024-12-25 19:00:00');
