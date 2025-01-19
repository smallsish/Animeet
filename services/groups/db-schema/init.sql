DROP TABLE IF EXISTS `group_user`;
DROP TABLE IF EXISTS `group`;

CREATE TABLE `group` (
  `group_id` int NOT NULL,
  `event_id` int NOT NULL,
  `name` varchar(32) NOT NULL,
  `max_capacity` int NOT NULL,
  `slots_left` int NOT NULL,
  `description` varchar(64) NOT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `group` (`group_id`, `event_id`, `name`, `max_capacity`, `slots_left`, `description`) 
VALUES 
(1, 1, 'Cosplay Enthusiasts', 5, 2, 'Group for cosplay lovers'),
(2, 1, 'JJK Fans', 5, 4, 'JJK is love, JJK is life'),
(3, 1, 'Just Got Isekai’d', 5, 4, 'Truck kun is our greatest enemy'),
(4, 2, 'Testing Enthusiasts', 15, 14, 'Group for testing lovers');

CREATE TABLE `group_user` (
  `group_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role` varchar(32) NOT NULL,
  `date_joined` datetime NOT NULL,
  `payment_status` varchar(16) NOT NULL,
  PRIMARY KEY (`group_id`, `user_id`),
  FOREIGN KEY (`group_id`) REFERENCES `group`(`group_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `group_user` VALUES 
(1, 1, 'member', '2024-09-28 10:32:12', 'unpaid'),  -- Entry with group_id 1 and user_id 1
(1, 1000, 'leader', '2024-09-28 10:32:12', 'unpaid'),
(1, 1001, 'member', '2024-09-30 11:39:18', 'unpaid'),
(2, 1002, 'leader', '2024-09-28 21:02:44', 'unpaid'),
(3, 2, 'leader', '2024-09-28 21:02:44', 'unpaid'),
(4, 3, 'leader', '2024-09-28 21:02:44', 'unpaid');