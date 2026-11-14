-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: bank
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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_no` bigint NOT NULL,
  `customer_id` int NOT NULL,
  `account_type` varchar(20) DEFAULT NULL,
  `opening_date` date DEFAULT NULL,
  `balance` decimal(12,2) DEFAULT NULL,
  `account_status` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`account_no`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1001001,1,'Savings','2025-04-10',25000.00,'Active'),(1001002,2,'Savings','2025-05-15',18000.00,'Active'),(1001003,3,'Current','2025-06-20',42000.00,'Active'),(1001004,4,'Savings','2025-07-05',12500.00,'Active'),(1001005,5,'Savings','2025-08-12',30000.00,'Active'),(1001006,6,'Current','2025-09-01',67345.00,'Active');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `customer_name` varchar(60) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Aarav Sharma','Male','9876501001','Hyderabad'),(2,'Ananya Reddy','Female','9876501002','Guntur'),(3,'Rahul Kumar','Male','9876501003','Vijayawada'),(4,'Priya Singh','Female','9876501004','Kurnool'),(5,'Imran Ali','Male','9876501005','Palnadu'),(6,'Sneha Rao','Female','9876501006','Ongole'),(7,'Rafiq','Female','9876501007','Palnadu');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `account_no` bigint DEFAULT NULL,
  `transaction_date` datetime DEFAULT NULL,
  `transaction_type` enum('Deposit','Withdrawal') DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `account_no` (`account_no`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`account_no`) REFERENCES `accounts` (`account_no`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1001001,'2025-04-10 10:00:00','Deposit',25000.00,'Opening balance'),(2,1001002,'2025-05-15 11:00:00','Deposit',20000.00,'Opening balance'),(3,1001002,'2025-05-20 12:00:00','Withdrawal',2000.00,'ATM withdrawal'),(4,1001003,'2025-06-20 09:30:00','Deposit',50000.00,'Opening balance'),(5,1001003,'2025-06-25 14:00:00','Withdrawal',8000.00,'Business expense'),(6,1001004,'2025-07-05 10:30:00','Deposit',15000.00,'Opening balance'),(7,1001004,'2025-07-10 16:00:00','Withdrawal',2500.00,'Cash withdrawal'),(8,1001005,'2025-08-12 09:00:00','Deposit',30000.00,'Opening balance'),(9,1001006,'2025-09-01 10:15:00','Deposit',60000.00,'Opening balance'),(10,1001006,'2025-09-05 13:20:00','Withdrawal',5000.00,'Office expenses'),(11,1001006,'2026-11-29 00:00:00','Deposit',12345.00,'Cash Deposit');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-29 20:54:35
