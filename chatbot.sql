-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: chatbot
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chatbot_usage`
--

DROP TABLE IF EXISTS `chatbot_usage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatbot_usage` (
  `usage_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `chatbot_name` varchar(40) DEFAULT NULL,
  `usage_hours` float DEFAULT NULL,
  `usage_frequency` varchar(20) DEFAULT NULL,
  `purpose` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`usage_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `chatbot_usage_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatbot_usage`
--

LOCK TABLES `chatbot_usage` WRITE;
/*!40000 ALTER TABLE `chatbot_usage` DISABLE KEYS */;
INSERT INTO `chatbot_usage` VALUES (1,1,'ChatGPT',2,'Daily','Doubt Clarification'),(2,2,'ChatGPT',1,'Daily','Homework'),(3,3,'Gemini',3,'Weekly','Programming'),(4,4,'ChatGPT',2,'Daily','Exam Preparation'),(5,5,'Gemini',1,'Weekly','Homework'),(6,6,'ChatGPT',3,'Daily','Exam Preparation'),(7,7,'Copilot',2,'Weekly','Programming'),(8,8,'Gemini',1,'Daily','Doubt Clarification'),(9,9,'ChatGPT',2,'Weekly','Homework'),(10,10,'Copilot',3,'Daily','Programming');
/*!40000 ALTER TABLE `chatbot_usage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `learning_benefit` varchar(30) DEFAULT NULL,
  `satisfaction` int DEFAULT NULL,
  `comments` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,1,'Highly Beneficial',5,'Improves understanding'),(2,2,'Beneficial',4,'Helps in homework'),(3,3,'Highly Beneficial',5,'Useful for coding'),(4,4,'Beneficial',4,'Helps in preparation'),(5,5,'Average',3,'Needs improvement'),(6,6,'Highly Beneficial',5,'Saves time'),(7,7,'Beneficial',4,'Useful examples'),(8,8,'Average',3,'Good explanations'),(9,9,'Beneficial',4,'Quick answers'),(10,10,'Highly Beneficial',5,'Improves learning');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preferences`
--

DROP TABLE IF EXISTS `preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preferences` (
  `preference_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `learning_method` varchar(40) DEFAULT NULL,
  `subject` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`preference_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `preferences_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preferences`
--

LOCK TABLES `preferences` WRITE;
/*!40000 ALTER TABLE `preferences` DISABLE KEYS */;
INSERT INTO `preferences` VALUES (1,1,'Text','Computer Science'),(2,2,'Text','Mathematics'),(3,3,'Examples','Computer Science'),(4,4,'Video','Biology'),(5,5,'Examples','Mathematics'),(6,6,'Text','Computer Science'),(7,7,'Examples','Physics'),(8,8,'Video','Biology'),(9,9,'Text','Mathematics'),(10,10,'Examples','Computer Science');
/*!40000 ALTER TABLE `preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL,
  `student_name` varchar(50) DEFAULT NULL,
  `class_name` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Ravi Kumar','XII','Male'),(2,'Sita Devi','XII','Female'),(3,'Rahul Sharma','XI','Male'),(4,'Priya Reddy','XII','Female'),(5,'Arun Kumar','XI','Male'),(6,'Anjali Rao','XII','Female'),(7,'Kiran Kumar','XI','Male'),(8,'Sneha Reddy','XII','Female'),(9,'Vijay Kumar','XI','Male'),(10,'Divya Rao','XII','Female');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-29 23:23:32
