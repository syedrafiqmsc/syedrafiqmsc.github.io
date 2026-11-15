-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: ipl
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
-- Table structure for table `batting`
--

DROP TABLE IF EXISTS `batting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `batting` (
  `batting_id` int NOT NULL,
  `match_id` int DEFAULT NULL,
  `player_id` int DEFAULT NULL,
  `runs` int DEFAULT NULL,
  `balls` int DEFAULT NULL,
  `fours` int DEFAULT NULL,
  `sixes` int DEFAULT NULL,
  PRIMARY KEY (`batting_id`),
  KEY `match_id` (`match_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `batting_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`),
  CONSTRAINT `batting_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `batting`
--

LOCK TABLES `batting` WRITE;
/*!40000 ALTER TABLE `batting` DISABLE KEYS */;
INSERT INTO `batting` VALUES (1,1,1,75,45,7,3),(2,1,3,60,38,5,2),(3,2,5,82,48,8,4),(4,2,7,65,40,6,2),(5,3,9,70,42,6,3),(6,3,1,55,35,5,2),(7,4,3,68,44,5,3),(8,4,5,50,36,4,2),(9,5,7,90,50,9,4),(10,5,9,72,43,7,3);
/*!40000 ALTER TABLE `batting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bowling`
--

DROP TABLE IF EXISTS `bowling`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bowling` (
  `bowling_id` int NOT NULL,
  `match_id` int DEFAULT NULL,
  `player_id` int DEFAULT NULL,
  `overs` decimal(4,1) DEFAULT NULL,
  `runs_conceded` int DEFAULT NULL,
  `wickets` int DEFAULT NULL,
  PRIMARY KEY (`bowling_id`),
  KEY `match_id` (`match_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `bowling_ibfk_1` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`),
  CONSTRAINT `bowling_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bowling`
--

LOCK TABLES `bowling` WRITE;
/*!40000 ALTER TABLE `bowling` DISABLE KEYS */;
INSERT INTO `bowling` VALUES (1,1,2,4.0,30,2),(2,1,4,4.0,35,1),(3,2,6,4.0,28,3),(4,2,8,4.0,38,1),(5,3,10,4.0,32,2),(6,3,2,4.0,40,1),(7,4,4,4.0,25,3),(8,4,6,4.0,30,2),(9,5,8,4.0,36,2),(10,5,10,4.0,42,1);
/*!40000 ALTER TABLE `bowling` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `match_id` int NOT NULL,
  `match_date` date DEFAULT NULL,
  `venue` varchar(50) DEFAULT NULL,
  `team1_id` int DEFAULT NULL,
  `team2_id` int DEFAULT NULL,
  `team1_runs` int DEFAULT NULL,
  `team2_runs` int DEFAULT NULL,
  `winner_team_id` int DEFAULT NULL,
  PRIMARY KEY (`match_id`),
  KEY `team1_id` (`team1_id`),
  KEY `team2_id` (`team2_id`),
  KEY `winner_team_id` (`winner_team_id`),
  CONSTRAINT `matches_ibfk_1` FOREIGN KEY (`team1_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `matches_ibfk_2` FOREIGN KEY (`team2_id`) REFERENCES `teams` (`team_id`),
  CONSTRAINT `matches_ibfk_3` FOREIGN KEY (`winner_team_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES (1,'2026-04-01','Hyderabad',1,2,180,170,1),(2,'2026-04-03','Mumbai',3,4,195,180,3),(3,'2026-04-05','Jaipur',5,1,175,160,5),(4,'2026-04-07','Chennai',2,3,165,150,2),(5,'2026-04-09','Bengaluru',4,5,190,185,4);
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `player_id` int NOT NULL,
  `player_name` varchar(50) DEFAULT NULL,
  `team_id` int DEFAULT NULL,
  `player_role` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`player_id`),
  KEY `team_id` (`team_id`),
  CONSTRAINT `players_ibfk_1` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,'SRH Player 1',1,'Batsman'),(2,'SRH Player 2',1,'Bowler'),(3,'CSK Player 1',2,'Batsman'),(4,'CSK Player 2',2,'All Rounder'),(5,'MI Player 1',3,'Batsman'),(6,'MI Player 2',3,'Bowler'),(7,'RCB Player 1',4,'Batsman'),(8,'RCB Player 2',4,'All Rounder'),(9,'RR Player 1',5,'Batsman'),(10,'RR Player 2',5,'Bowler');
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `team_id` int NOT NULL,
  `team_code` varchar(10) DEFAULT NULL,
  `team_name` varchar(50) DEFAULT NULL,
  `home_city` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE KEY `team_code` (`team_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES (1,'SRH','Sunrisers Hyderabad','Hyderabad'),(2,'CSK','Chennai Super Kings','Chennai'),(3,'MI','Mumbai Indians','Mumbai'),(4,'RCB','Royal Challengers Bengaluru','Bengaluru'),(5,'RR','Rajasthan Royals','Jaipur');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-30  2:31:07
