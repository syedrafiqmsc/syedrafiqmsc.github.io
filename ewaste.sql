-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: ewaste
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
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `collection_id` int NOT NULL AUTO_INCREMENT,
  `item_name` varchar(100) NOT NULL,
  `category_id` int NOT NULL,
  `quantity_kg` decimal(10,2) NOT NULL,
  `collection_date` date NOT NULL,
  `collection_location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`collection_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `collections_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `waste_categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (1,'Old Desktop Computers',1,25.50,'2026-11-10','School Computer Lab'),(2,'Damaged Mobile Phones',2,8.00,'2026-11-11','Collection Centre'),(3,'Used Batteries',3,12.50,'2026-11-12','Science Lab'),(4,'Old Television Sets',4,35.00,'2026-11-13','Community Centre'),(5,'Old Printers',5,18.00,'2026-11-14','School Office');
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disposal_methods`
--

DROP TABLE IF EXISTS `disposal_methods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disposal_methods` (
  `method_id` int NOT NULL AUTO_INCREMENT,
  `method_name` varchar(50) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`method_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disposal_methods`
--

LOCK TABLES `disposal_methods` WRITE;
/*!40000 ALTER TABLE `disposal_methods` DISABLE KEYS */;
INSERT INTO `disposal_methods` VALUES (1,'Recycling','Recovering useful materials'),(2,'Reuse','Repairing and reusing electronic items'),(3,'Safe Disposal','Disposal through authorised facilities'),(4,'Refurbishment','Restoring old electronic equipment');
/*!40000 ALTER TABLE `disposal_methods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `disposal_records`
--

DROP TABLE IF EXISTS `disposal_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `disposal_records` (
  `disposal_id` int NOT NULL AUTO_INCREMENT,
  `collection_id` int NOT NULL,
  `method_id` int NOT NULL,
  `quantity_kg` decimal(10,2) NOT NULL,
  `disposal_date` date NOT NULL,
  `remarks` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`disposal_id`),
  KEY `collection_id` (`collection_id`),
  KEY `method_id` (`method_id`),
  CONSTRAINT `disposal_records_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`collection_id`),
  CONSTRAINT `disposal_records_ibfk_2` FOREIGN KEY (`method_id`) REFERENCES `disposal_methods` (`method_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `disposal_records`
--

LOCK TABLES `disposal_records` WRITE;
/*!40000 ALTER TABLE `disposal_records` DISABLE KEYS */;
INSERT INTO `disposal_records` VALUES (1,1,1,20.00,'2026-11-15','Sent for recycling'),(2,2,2,5.00,'2026-11-15','Reusable components recovered'),(3,3,3,10.00,'2026-11-16','Sent for safe disposal'),(4,4,1,25.00,'2026-11-16','Materials sent for recycling'),(5,5,4,12.00,'2026-11-17','Sent for refurbishment');
/*!40000 ALTER TABLE `disposal_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `waste_categories`
--

DROP TABLE IF EXISTS `waste_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `waste_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `waste_categories`
--

LOCK TABLES `waste_categories` WRITE;
/*!40000 ALTER TABLE `waste_categories` DISABLE KEYS */;
INSERT INTO `waste_categories` VALUES (1,'Computers','Old computers and laptops'),(2,'Mobile Phones','Discarded mobile phones'),(3,'Batteries','Used electronic batteries'),(4,'Televisions','Old television sets'),(5,'Printers','Discarded printers and scanners');
/*!40000 ALTER TABLE `waste_categories` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-29 21:36:58
