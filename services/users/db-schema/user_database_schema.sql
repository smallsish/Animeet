--CREATE DATABASE `user` ;

USE `user`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `dateOfBirth` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES (1,'kevinksaji10@gmail.com','Kevin Saji','1990-01-15'),(2,'jane.smith@example.com','jane_smith','1985-06-23'),(3,'alice.walker@example.com','alice_walker','1992-09-10'),
(1000,'john.smith@example.com','john_smith','1985-06-23'),(1001,'alan.walker@example.com','alan_walker','1995-03-10'),
(1002,'peter.parker@example.com','peter_parker','1999-01-21');
UNLOCK TABLES;
