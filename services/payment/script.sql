-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Database: payment
-- ------------------------------------------------------
-- Server version	8.0.23

-- CREATE DATABASE /*!32312 IF NOT EXISTS*/ `payment` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- USE `payment`;

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` varchar(64) NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `payment` (`payment_id`, `user_id`, `group_id`, `date`) 
VALUES 
('d73357d8-8a9e-4a4c-8b93-e3b403bd643a', 1, 1, '2024-10-10 14:00:00');

--
-- Table structure for table `payment`
--

-- DROP TABLE IF EXISTS `payment`;

-- CREATE TABLE `payment` (
--   `pid` varchar(64) NOT NULL,
--   `uid` int NOT NULL,
--   `gid` int NOT NULL,
--   `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (`pid`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --
-- -- Dumping data for table `payment`
-- --

-- INSERT INTO `payment` (`pid`, `uid`, `gid`, `date`) 
-- VALUES 
-- ('d73357d8-8a9e-4a4c-8b93-e3b403bd643a', 1, 1, '2024-10-10 14:00:00');

-- Dump completed on 2024-10-10

