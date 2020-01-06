-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: my_first_db1
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CIELAB`
--

DROP TABLE IF EXISTS `CIELAB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CIELAB` (
  `userid` int PRIMARY KEY AUTO_INCREMENT,
  `type` char(10) DEFAULT NULL,
  `fruit_id` varchar(255) DEFAULT NULL,
  `box_no` int(11) DEFAULT NULL,
  `L_value` float(10,4) DEFAULT NULL,
  `a_value` float(10,4) DEFAULT NULL,
  `b_value` float(10,4) DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `minor_axis` float(10,4) DEFAULT NULL,
  `major_axis` float(10,4) DEFAULT NULL,
  `size` float(10,4) DEFAULT NULL,
  `cheek_size` float(10,4) DEFAULT NULL,
  `shoulder_size` float(10,4) DEFAULT NULL,
  `count_spots` int(11) DEFAULT NULL,
  `count_mango` int(11) DEFAULT NULL,
  `ratio` float(10,4) DEFAULT NULL,
  `ratio_spots` float(10,4) DEFAULT NULL,
  `shelf_life` float(10,4) DEFAULT NULL,
  `grade_quality` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Results_full_classifier`
--

DROP TABLE IF EXISTS `Results_full_classifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Results_full_classifier` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `img_name` varchar(255) DEFAULT NULL,
  `prediction` varchar(255) DEFAULT NULL,
  `stage1` float(10,2) DEFAULT NULL,
  `stage2` float(10,2) DEFAULT NULL,
  `stage3` float(10,2) DEFAULT NULL,
  `stage4` float(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Results_skin_classifier`
--

DROP TABLE IF EXISTS `Results_skin_classifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Results_skin_classifier` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `img_name` varchar(255) DEFAULT NULL,
  `prediction` varchar(255) DEFAULT NULL,
  `stage1` float(10,2) DEFAULT NULL,
  `stage2` float(10,2) DEFAULT NULL,
  `stage3` float(10,2) DEFAULT NULL,
  `stage4` float(10,2) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-06 19:11:04
