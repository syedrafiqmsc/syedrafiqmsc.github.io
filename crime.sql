-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: crime
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
-- Current Database: `crime`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `crime` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `crime`;

--
-- Table structure for table `awareness_tips`
--

DROP TABLE IF EXISTS `awareness_tips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `awareness_tips` (
  `tip_id` int NOT NULL,
  `tip_title` varchar(100) DEFAULT NULL,
  `tip_description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`tip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `awareness_tips`
--

LOCK TABLES `awareness_tips` WRITE;
/*!40000 ALTER TABLE `awareness_tips` DISABLE KEYS */;
INSERT INTO `awareness_tips` VALUES (1,'Strong Passwords','Use strong and unique passwords.'),(2,'OTP Safety','Never share OTP with anyone.'),(3,'UPI Safety','Never enter UPI PIN to receive money.'),(4,'Email Safety','Avoid clicking suspicious email links.'),(5,'Social Media Safety','Do not share personal information publicly.'),(6,'Secure Websites','Check HTTPS before entering information.'),(7,'Unknown Links','Avoid downloading unknown attachments.'),(8,'Report Cybercrime','Report cybercrime through official channels.');
/*!40000 ALTER TABLE `awareness_tips` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL,
  `category_name` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Phishing','Fake emails and messages'),(2,'Online Fraud','Fraud through internet'),(3,'Identity Theft','Misuse of personal identity'),(4,'Cyber Bullying','Harassment through internet'),(5,'Hacking','Unauthorized system access'),(6,'UPI Fraud','Fraud through UPI payments'),(7,'Data Theft','Stealing confidential data'),(8,'Social Media Fraud','Fraud using social media');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incidents`
--

DROP TABLE IF EXISTS `incidents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incidents` (
  `incident_id` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `incident_date` date DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `loss_amount` decimal(12,2) DEFAULT NULL,
  `case_status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`incident_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `incidents_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incidents`
--

LOCK TABLES `incidents` WRITE;
/*!40000 ALTER TABLE `incidents` DISABLE KEYS */;
INSERT INTO `incidents` VALUES (101,1,'2026-01-05','Andhra Pradesh',5000.00,'Pending'),(102,2,'2026-01-12','Telangana',12000.00,'Resolved'),(103,3,'2026-02-08','Karnataka',8000.00,'Pending'),(104,4,'2026-02-15','Andhra Pradesh',0.00,'Under Investigation'),(105,5,'2026-03-10','Tamil Nadu',15000.00,'Resolved'),(106,6,'2026-03-18','Andhra Pradesh',25000.00,'Pending'),(107,7,'2026-04-05','Kerala',18000.00,'Under Investigation'),(108,8,'2026-04-20','Telangana',7000.00,'Resolved'),(109,1,'2026-05-11','Karnataka',6000.00,'Pending'),(110,6,'2026-05-25','Andhra Pradesh',10000.00,'Resolved');
/*!40000 ALTER TABLE `incidents` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-29 22:17:35
