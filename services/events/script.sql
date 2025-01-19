-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Database: event
-- ------------------------------------------------------
-- Server version	8.0.23

--
-- Table structure for table `event`
--

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `event`
--

INSERT INTO `event` VALUES (1,'Music Concert','City Hall',50,'An evening of classical music with a live orchestra.',50,50,'2024-12-25 19:00:00');

-- Dump completed on 2021-08-15  1:38:38