-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: socialmedia
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
-- Table structure for table `platforms`
--

DROP TABLE IF EXISTS `platforms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platforms` (
  `platform_id` int NOT NULL,
  `platform_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`platform_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platforms`
--

LOCK TABLES `platforms` WRITE;
/*!40000 ALTER TABLE `platforms` DISABLE KEYS */;
INSERT INTO `platforms` VALUES (1,'Instagram'),(2,'WhatsApp'),(3,'YouTube'),(4,'Facebook'),(5,'Snapchat');
/*!40000 ALTER TABLE `platforms` ENABLE KEYS */;
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
  `class_name` varchar(20) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Aman','XII','Male'),(2,'Rahul','XII','Male'),(3,'Priya','XII','Female'),(4,'Anjali','XI','Female'),(5,'Kiran','XI','Male'),(6,'Sneha','XII','Female'),(7,'Arjun','XI','Male'),(8,'Divya','XII','Female'),(9,'Ravi','XI','Male'),(10,'Pooja','XII','Female');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usage_records`
--

DROP TABLE IF EXISTS `usage_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usage_records` (
  `usage_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `platform_id` int DEFAULT NULL,
  `usage_date` date DEFAULT NULL,
  `screen_hours` decimal(4,2) DEFAULT NULL,
  `daily_sessions` int DEFAULT NULL,
  PRIMARY KEY (`usage_id`),
  KEY `student_id` (`student_id`),
  KEY `platform_id` (`platform_id`),
  CONSTRAINT `usage_records_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `usage_records_ibfk_2` FOREIGN KEY (`platform_id`) REFERENCES `platforms` (`platform_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usage_records`
--

LOCK TABLES `usage_records` WRITE;
/*!40000 ALTER TABLE `usage_records` DISABLE KEYS */;
INSERT INTO `usage_records` VALUES (1,1,1,'2026-11-01',3.50,12),(2,2,2,'2026-11-01',2.00,10),(3,3,3,'2026-11-01',4.00,8),(4,4,1,'2026-11-01',2.50,9),(5,5,4,'2026-11-01',1.50,6),(6,6,5,'2026-11-01',3.00,11),(7,7,3,'2026-11-01',2.00,7),(8,8,1,'2026-11-01',5.00,15),(9,9,2,'2026-11-01',1.00,5),(10,10,3,'2026-11-01',4.50,13),(11,1,2,'2026-11-02',1.50,8),(12,2,3,'2026-11-02',2.50,9),(13,3,1,'2026-11-02',3.00,10),(14,4,5,'2026-11-02',2.00,7),(15,5,3,'2026-11-02',1.00,5),(16,6,1,'2026-11-02',2.50,9),(17,7,4,'2026-11-02',1.50,6),(18,8,2,'2026-11-02',4.00,14),(19,9,3,'2026-11-02',2.00,8),(20,10,1,'2026-11-02',3.50,12);
/*!40000 ALTER TABLE `usage_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wellbeing`
--

DROP TABLE IF EXISTS `wellbeing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wellbeing` (
  `wellbeing_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `record_date` date DEFAULT NULL,
  `sleep_hours` decimal(4,2) DEFAULT NULL,
  `study_hours` decimal(4,2) DEFAULT NULL,
  `concentration` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`wellbeing_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `wellbeing_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wellbeing`
--

LOCK TABLES `wellbeing` WRITE;
/*!40000 ALTER TABLE `wellbeing` DISABLE KEYS */;
INSERT INTO `wellbeing` VALUES (1,1,'2026-11-01',7.00,3.00,'Good'),(2,2,'2026-11-01',8.00,4.00,'Good'),(3,3,'2026-11-01',6.00,2.00,'Average'),(4,4,'2026-11-01',7.50,4.00,'Good'),(5,5,'2026-11-01',8.00,5.00,'Good'),(6,6,'2026-11-01',6.50,3.00,'Average'),(7,7,'2026-11-01',7.00,4.00,'Good'),(8,8,'2026-11-01',5.50,2.00,'Poor'),(9,9,'2026-11-01',8.00,5.00,'Good'),(10,10,'2026-11-01',6.00,2.50,'Average');
/*!40000 ALTER TABLE `wellbeing` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-30  2:56:30
