-- Drop the payment table if it exists to ensure a clean setup
DROP TABLE IF EXISTS `payment`;

-- Create the `payment` table
CREATE TABLE `payment` (
    `payment_id` varchar(64) NOT NULL,
    `user_id` int NOT NULL,
    `group_id` int NOT NULL,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insert initial test data into the `payment` table
INSERT INTO `payment` 
VALUES 
    ('c3a57b8e-1d8c-4f21-84c7-b2b7c0f2a2d3', 2, 1, '2024-10-11 14:00:00'),
    ('f8c7b1f8-4c18-49a9-8b7f-abc62df11a45', 3, 2, '2024-10-12 15:00:00');