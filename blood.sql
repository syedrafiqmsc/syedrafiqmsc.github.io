-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: blood
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
-- Table structure for table `bloodrequest`
--

DROP TABLE IF EXISTS `bloodrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloodrequest` (
  `RequestID` int NOT NULL AUTO_INCREMENT,
  `RequesterName` varchar(50) DEFAULT NULL,
  `BloodGroup` varchar(3) DEFAULT NULL,
  `UnitsRequested` int DEFAULT NULL,
  `RequestDate` date DEFAULT NULL,
  `Status` varchar(15) DEFAULT 'Pending',
  PRIMARY KEY (`RequestID`),
  KEY `BloodGroup` (`BloodGroup`),
  CONSTRAINT `bloodrequest_ibfk_1` FOREIGN KEY (`BloodGroup`) REFERENCES `bloodstock` (`BloodGroup`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloodrequest`
--

LOCK TABLES `bloodrequest` WRITE;
/*!40000 ALTER TABLE `bloodrequest` DISABLE KEYS */;
INSERT INTO `bloodrequest` VALUES (1,'City Hospital','O+',1,'2026-11-29','Pending'),(2,'Apollo','A',3,'2026-11-29','Pending');
/*!40000 ALTER TABLE `bloodrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bloodstock`
--

DROP TABLE IF EXISTS `bloodstock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bloodstock` (
  `BloodGroup` varchar(3) NOT NULL,
  `UnitsAvailable` int DEFAULT '0',
  PRIMARY KEY (`BloodGroup`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bloodstock`
--

LOCK TABLES `bloodstock` WRITE;
/*!40000 ALTER TABLE `bloodstock` DISABLE KEYS */;
INSERT INTO `bloodstock` VALUES ('A',0),('A-',0),('A+',2),('AB-',0),('AB+',0),('B-',0),('B+',0),('O-',0),('O+',0);
/*!40000 ALTER TABLE `bloodstock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation`
--

DROP TABLE IF EXISTS `donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation` (
  `DonationID` int NOT NULL AUTO_INCREMENT,
  `DonorID` int DEFAULT NULL,
  `DonationDate` date DEFAULT NULL,
  `BloodGroup` varchar(3) DEFAULT NULL,
  `UnitsDonated` int DEFAULT NULL,
  PRIMARY KEY (`DonationID`),
  KEY `DonorID` (`DonorID`),
  CONSTRAINT `donation_ibfk_1` FOREIGN KEY (`DonorID`) REFERENCES `donor` (`DonorID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation`
--

LOCK TABLES `donation` WRITE;
/*!40000 ALTER TABLE `donation` DISABLE KEYS */;
INSERT INTO `donation` VALUES (1,1,'2026-11-29','O+',1),(2,4,'2026-11-29','A+',2);
/*!40000 ALTER TABLE `donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor`
--

DROP TABLE IF EXISTS `donor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor` (
  `DonorID` int NOT NULL AUTO_INCREMENT,
  `DonorName` varchar(50) NOT NULL,
  `Age` int DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `BloodGroup` varchar(3) DEFAULT NULL,
  `City` varchar(50) DEFAULT NULL,
  `RegistrationDate` date DEFAULT NULL,
  PRIMARY KEY (`DonorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor`
--

LOCK TABLES `donor` WRITE;
/*!40000 ALTER TABLE `donor` DISABLE KEYS */;
INSERT INTO `donor` VALUES (1,'Aarav Kumar',25,'9000000001','O+','Palnadu','2026-07-01'),(2,'Sana Begum',29,'9000000002','B+','Guntur','2026-07-04'),(3,'Ravi Teja',34,'9000000003','A+','Narasaraopet','2026-07-10'),(4,'Rafiq',45,'9704017704','A+','Kurnool','2026-11-29');
/*!40000 ALTER TABLE `donor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-29 10:10:42
