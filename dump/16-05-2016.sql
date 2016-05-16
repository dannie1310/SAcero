-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: control_acero
-- ------------------------------------------------------
-- Server version	5.6.28-log

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add material',7,'add_material'),(20,'Can change material',7,'change_material'),(21,'Can delete material',7,'delete_material'),(22,'Can add despiece',8,'add_despiece'),(23,'Can change despiece',8,'change_despiece'),(24,'Can delete despiece',8,'delete_despiece'),(25,'Can add elemento',9,'add_elemento'),(26,'Can change elemento',9,'change_elemento'),(27,'Can delete elemento',9,'delete_elemento'),(34,'Can add transporte',12,'add_transporte'),(35,'Can change transporte',12,'change_transporte'),(36,'Can delete transporte',12,'delete_transporte'),(37,'Can add taller',13,'add_taller'),(38,'Can change taller',13,'change_taller'),(39,'Can delete taller',13,'delete_taller'),(40,'Can add funcion',14,'add_funcion'),(41,'Can change funcion',14,'change_funcion'),(42,'Can delete funcion',14,'delete_funcion'),(43,'Can add frente',15,'add_frente'),(44,'Can change frente',15,'change_frente'),(45,'Can delete frente',15,'delete_frente'),(46,'Can add control asignacion',16,'add_controlasignacion'),(47,'Can change control asignacion',16,'change_controlasignacion'),(48,'Can delete control asignacion',16,'delete_controlasignacion'),(55,'Can add apoyo',19,'add_apoyo'),(56,'Can change apoyo',19,'change_apoyo'),(57,'Can delete apoyo',19,'delete_apoyo'),(61,'Can add programa suministro',21,'add_programasuministro'),(62,'Can change programa suministro',21,'change_programasuministro'),(63,'Can delete programa suministro',21,'delete_programasuministro'),(64,'Can add programa suministro detalle',22,'add_programasuministrodetalle'),(65,'Can change programa suministro detalle',22,'change_programasuministrodetalle'),(66,'Can delete programa suministro detalle',22,'delete_programasuministrodetalle'),(67,'Can add etapa asignacion',23,'add_etapaasignacion'),(68,'Can change etapa asignacion',23,'change_etapaasignacion'),(69,'Can delete etapa asignacion',23,'delete_etapaasignacion'),(70,'Can add modulo',24,'add_modulo'),(71,'Can change modulo',24,'change_modulo'),(72,'Can delete modulo',24,'delete_modulo'),(73,'Can add grupo',25,'add_grupo'),(74,'Can change grupo',25,'change_grupo'),(75,'Can delete grupo',25,'delete_grupo'),(76,'Can add archivo',26,'add_archivo'),(77,'Can change archivo',26,'change_archivo'),(78,'Can delete archivo',26,'delete_archivo'),(82,'Can add factor',28,'add_factor'),(83,'Can change factor',28,'change_factor'),(84,'Can delete factor',28,'delete_factor');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$Ixmwtp7N2ztz$Z8rF2yZ8i5NHyn7EzUMEMkUYUpmyNJmEIF2gXGhxeZ8=','2016-04-21 22:51:58',1,'rjimenez','','','patolin00755@hotmail.com',1,1,'2016-04-18 19:29:59'),(2,'pbkdf2_sha256$20000$pPJzRtlXObNS$yDVBvY97sDPC2Htth3tyXhr9MHJVbw9RFkXkq5vJ8pM=','2016-05-04 23:46:06',1,'roman.jimenez.estrada','','','patolin00755@hotmail.com',1,1,'2016-04-21 22:32:15'),(4,'pbkdf2_sha256$20000$PktfFzGDl2Qr$7fV6ntiS/j2cwCTnHX+7ITAXAe2VvymXzkoMI1DujBg=','2016-04-27 23:35:34',0,'prueba','','','',1,1,'2016-04-27 23:34:21'),(5,'pbkdf2_sha256$20000$U1lepeirBwmN$635357qW0nwoHLQxp1zwVWiw+lYakZBDtmmZMZ9hYaU=','2016-05-04 23:47:00',1,'dbenitezc','','','',1,1,'2016-05-04 23:43:24'),(6,'pbkdf2_sha256$20000$fHhtUMPh0gfl$dBGyVbLXlE19tX9D6M32Eq8bj4fPVnAphoPmFPdJErU=',NULL,0,'test','','','',0,1,'2016-05-12 23:22:00');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
INSERT INTO `auth_user_user_permissions` VALUES (3,4,55);
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_apoyo`
--

DROP TABLE IF EXISTS `control_acero_apoyo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_apoyo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` varchar(100) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_apoyo`
--

LOCK TABLES `control_acero_apoyo` WRITE;
/*!40000 ALTER TABLE `control_acero_apoyo` DISABLE KEYS */;
INSERT INTO `control_acero_apoyo` VALUES (1,'111',1,'2016-05-02 17:22:02','2016-04-29 00:10:20'),(2,'30',1,'2016-05-02 16:42:03','2016-05-02 16:42:03'),(3,'31',1,'2016-05-02 16:42:38','2016-05-02 16:42:38'),(4,'32',1,'2016-05-02 16:43:47','2016-05-02 16:43:47'),(5,'33',1,'2016-05-02 16:44:38','2016-05-02 16:44:38'),(6,'34',1,'2016-05-02 16:45:19','2016-05-02 16:45:19'),(7,'35',1,'2016-05-02 16:46:56','2016-05-02 16:46:40'),(8,'36',1,'2016-05-04 16:04:23','2016-05-02 16:50:56'),(9,'37',1,'2016-05-04 16:05:17','2016-05-02 16:51:58'),(10,'38',1,'2016-05-04 16:05:26','2016-05-02 16:52:13'),(11,'39',1,'2016-05-04 16:05:45','2016-05-02 16:52:19'),(12,'40',1,'2016-05-04 16:05:55','2016-05-02 16:52:28'),(13,'41',1,'2016-05-04 16:06:11','2016-05-02 16:52:37'),(14,'42',1,'2016-05-04 16:06:20','2016-05-02 16:53:04'),(15,'43',1,'2016-05-04 16:06:28','2016-05-02 16:53:12'),(16,'51',1,'2016-05-04 16:13:50','2016-05-02 16:53:49'),(17,'52',1,'2016-05-04 16:13:59','2016-05-02 16:53:56'),(18,'53',1,'2016-05-04 16:13:38','2016-05-02 16:54:03'),(19,'54',1,'2016-05-04 16:14:06','2016-05-02 16:54:11'),(20,'55',1,'2016-05-04 16:14:30','2016-05-02 16:54:21'),(21,'56',1,'2016-05-04 16:14:38','2016-05-02 16:54:32'),(22,'88',1,'2016-05-04 15:59:30','2016-05-02 16:58:03'),(23,'89',1,'2016-05-04 15:59:42','2016-05-02 16:59:07'),(24,'90',1,'2016-05-04 15:59:53','2016-05-02 17:04:40'),(25,'91',1,'2016-05-04 16:00:01','2016-05-02 17:05:18'),(26,'92',1,'2016-05-04 16:00:11','2016-05-02 17:05:37'),(27,'93',1,'2016-05-04 16:00:18','2016-05-02 17:05:49'),(28,'94',1,'2016-05-04 16:00:27','2016-05-02 17:06:08'),(29,'95',1,'2016-05-04 16:00:37','2016-05-02 17:06:26'),(30,'96',1,'2016-05-04 16:00:43','2016-05-02 17:07:04'),(31,'97',1,'2016-05-04 16:00:53','2016-05-02 17:07:30'),(32,'98',1,'2016-05-04 16:01:00','2016-05-02 17:07:43'),(33,'99',1,'2016-05-04 16:01:07','2016-05-02 17:08:06'),(34,'100',1,'2016-05-04 16:01:22','2016-05-02 17:08:46'),(35,'101',1,'2016-05-02 17:10:33','2016-05-02 17:09:40'),(36,'102',1,'2016-05-02 17:10:29','2016-05-02 17:10:29'),(37,'103',1,'2016-05-02 17:35:57','2016-05-02 17:19:00'),(38,'104',1,'2016-05-02 17:36:05','2016-05-02 17:19:16'),(39,'105',1,'2016-05-02 17:36:09','2016-05-02 17:19:27'),(40,'106',1,'2016-05-02 17:27:25','2016-05-02 17:19:37'),(41,'107',1,'2016-05-02 17:27:30','2016-05-02 17:19:44'),(42,'108',1,'2016-05-02 17:23:55','2016-05-02 17:19:55'),(43,'119',1,'2016-05-02 17:32:39','2016-05-02 17:20:04'),(44,'120',1,'2016-05-02 17:36:25','2016-05-02 17:20:30'),(45,'121',1,'2016-05-02 17:36:33','2016-05-02 17:21:06'),(46,'122',1,'2016-05-02 17:36:38','2016-05-02 17:21:14'),(47,'123',1,'2016-05-02 17:36:43','2016-05-02 17:21:25'),(48,'124',1,'2016-05-02 17:36:48','2016-05-02 17:21:41'),(49,'110',1,'2016-05-02 17:24:30','2016-05-02 17:21:55'),(50,'112',1,'2016-05-02 17:24:42','2016-05-02 17:22:10'),(51,'113',1,'2016-05-02 17:24:48','2016-05-02 17:22:21'),(52,'114',1,'2016-05-02 17:24:56','2016-05-02 17:22:28'),(53,'115',1,'2016-05-02 17:25:00','2016-05-02 17:22:35'),(54,'109',1,'2016-05-02 17:27:41','2016-05-02 17:24:20'),(55,'116',1,'2016-05-02 17:25:44','2016-05-02 17:25:21'),(56,'117',1,'2016-05-02 17:25:26','2016-05-02 17:25:26'),(57,'118',1,'2016-05-02 17:25:34','2016-05-02 17:25:34'),(58,'125',1,'2016-05-04 16:01:34','2016-05-02 17:28:43'),(59,'126',1,'2016-05-04 16:08:17','2016-05-02 17:35:19'),(60,'127',1,'2016-05-04 16:08:30','2016-05-02 17:35:27'),(61,'128',1,'2016-05-04 16:08:52','2016-05-02 17:35:34'),(62,'129',1,'2016-05-04 16:08:37','2016-05-02 17:35:45'),(63,'130',1,'2016-05-04 16:08:44','2016-05-02 17:37:01'),(64,'142',1,'2016-05-04 16:11:04','2016-05-02 17:37:26'),(65,'143',1,'2016-05-04 16:17:46','2016-05-02 17:37:38'),(66,'144',1,'2016-05-04 16:17:39','2016-05-02 17:37:54'),(67,'145',1,'2016-05-04 16:17:30','2016-05-02 17:38:12'),(68,'146',1,'2016-05-04 16:17:25','2016-05-02 17:38:29'),(69,'147',1,'2016-05-04 16:17:18','2016-05-02 17:38:44'),(70,'148',1,'2016-05-04 16:16:53','2016-05-02 17:39:01'),(71,'149',1,'2016-05-04 16:15:44','2016-05-02 17:39:15'),(72,'150',1,'2016-05-04 16:15:34','2016-05-02 17:39:27'),(73,'131',1,'2016-05-04 14:26:05','2016-05-04 14:26:05'),(74,'132',1,'2016-05-04 16:09:27','2016-05-04 14:27:02'),(75,'133',1,'2016-05-04 16:09:41','2016-05-04 14:27:22'),(76,'134',1,'2016-05-04 16:09:46','2016-05-04 14:27:28'),(77,'135',1,'2016-05-04 16:10:06','2016-05-04 14:27:32'),(78,'136',1,'2016-05-04 16:10:12','2016-05-04 14:27:37'),(79,'137',1,'2016-05-04 16:10:18','2016-05-04 14:27:42'),(81,'138',1,'2016-05-04 16:10:26','2016-05-04 14:41:28'),(82,'139',1,'2016-05-04 16:10:39','2016-05-04 14:41:32'),(83,'140',1,'2016-05-04 16:10:46','2016-05-04 14:42:11'),(84,'141',1,'2016-05-04 16:10:52','2016-05-04 14:42:18'),(85,'44',1,'2016-05-04 16:07:17','2016-05-04 15:56:30'),(86,'47',1,'2016-05-04 16:07:29','2016-05-04 15:57:41'),(87,'49',1,'2016-05-04 16:07:43','2016-05-04 15:57:48'),(88,'50',1,'2016-05-04 16:07:57','2016-05-04 15:57:54');
/*!40000 ALTER TABLE `control_acero_apoyo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_apoyo_elemento`
--

DROP TABLE IF EXISTS `control_acero_apoyo_elemento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_apoyo_elemento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apoyo_id` int(11) NOT NULL,
  `elemento_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `apoyo_id` (`apoyo_id`,`elemento_id`),
  KEY `control_acero__elemento_id_528f2c56_fk_control_acero_elemento_id` (`elemento_id`),
  CONSTRAINT `control_acero__elemento_id_528f2c56_fk_control_acero_elemento_id` FOREIGN KEY (`elemento_id`) REFERENCES `control_acero_elemento` (`id`),
  CONSTRAINT `control_acero_apoyo__apoyo_id_1f3383a2_fk_control_acero_apoyo_id` FOREIGN KEY (`apoyo_id`) REFERENCES `control_acero_apoyo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_apoyo_elemento`
--

LOCK TABLES `control_acero_apoyo_elemento` WRITE;
/*!40000 ALTER TABLE `control_acero_apoyo_elemento` DISABLE KEYS */;
INSERT INTO `control_acero_apoyo_elemento` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,2,1),(6,2,3),(7,2,4),(8,2,6),(9,3,1),(10,3,3),(11,3,4),(12,3,6),(13,4,1),(14,4,3),(15,4,4),(16,4,6),(17,5,1),(18,5,3),(19,5,4),(20,5,6),(21,6,1),(22,6,3),(23,6,4),(24,6,6),(25,7,1),(26,7,3),(28,7,4),(27,7,6),(29,8,1),(196,8,3),(235,8,4),(197,8,6),(236,9,3),(237,9,4),(199,9,6),(30,9,7),(238,10,3),(239,10,4),(200,10,6),(31,10,7),(240,11,3),(241,11,4),(201,11,6),(32,11,7),(242,12,3),(243,12,4),(202,12,6),(33,12,7),(244,13,3),(245,13,4),(203,13,6),(34,13,7),(246,14,3),(247,14,4),(204,14,6),(35,14,7),(248,15,3),(249,15,4),(205,15,6),(36,15,7),(315,16,3),(37,16,4),(316,16,6),(210,16,7),(317,17,3),(38,17,4),(318,17,6),(211,17,7),(313,18,3),(39,18,4),(314,18,6),(212,18,7),(319,19,3),(40,19,4),(320,19,6),(213,19,7),(321,20,3),(41,20,4),(322,20,6),(214,20,7),(323,21,3),(42,21,4),(324,21,6),(215,21,7),(47,22,1),(45,22,3),(216,22,4),(50,22,6),(48,23,3),(217,23,4),(49,23,6),(46,23,8),(52,24,3),(218,24,4),(53,24,6),(51,24,8),(54,25,1),(55,25,3),(219,25,4),(56,25,6),(57,26,1),(58,26,3),(220,26,4),(59,26,6),(60,27,1),(61,27,3),(221,27,4),(62,27,6),(63,28,1),(64,28,3),(222,28,4),(65,28,6),(66,29,1),(67,29,2),(68,29,3),(223,29,4),(69,30,2),(70,30,3),(224,30,4),(71,30,5),(72,31,2),(73,31,3),(225,31,4),(74,31,5),(75,32,2),(76,32,3),(226,32,4),(77,32,5),(78,33,2),(79,33,3),(227,33,4),(80,33,5),(81,34,2),(82,34,3),(228,34,4),(83,34,5),(84,35,2),(85,35,3),(86,35,4),(87,35,5),(88,36,2),(89,36,3),(90,36,4),(91,36,5),(126,37,2),(138,37,3),(153,37,4),(92,37,5),(127,38,2),(139,38,3),(154,38,4),(93,38,5),(128,39,2),(140,39,3),(155,39,4),(94,39,5),(110,40,2),(113,40,3),(129,40,4),(95,40,5),(111,41,2),(114,41,3),(130,41,4),(96,41,5),(112,42,2),(115,42,3),(97,42,5),(132,43,3),(141,43,4),(125,43,6),(100,43,7),(142,44,3),(156,44,4),(133,44,6),(99,44,7),(143,45,3),(157,45,4),(134,45,6),(101,45,7),(144,46,3),(158,46,4),(102,46,7),(145,47,3),(159,47,4),(135,47,6),(103,47,7),(146,48,3),(160,48,4),(136,48,6),(104,48,7),(105,49,3),(117,49,4),(106,50,3),(118,50,4),(107,51,3),(119,51,4),(108,52,3),(120,52,4),(109,53,3),(121,53,4),(116,54,3),(131,54,4),(122,55,4),(123,56,4),(124,57,4),(147,58,3),(229,58,4),(137,58,6),(148,58,7),(262,59,3),(263,59,4),(230,59,6),(149,59,7),(264,60,3),(265,60,4),(231,60,6),(150,60,7),(270,61,3),(271,61,4),(232,61,6),(151,61,7),(266,62,3),(267,62,4),(233,62,6),(152,62,7),(268,63,3),(269,63,4),(234,63,6),(161,63,7),(302,64,3),(162,64,4),(303,64,6),(193,64,7),(198,65,1),(304,65,3),(163,65,4),(305,65,6),(164,66,3),(165,66,4),(331,66,6),(306,66,8),(307,67,1),(166,67,3),(167,67,4),(330,67,6),(168,68,3),(169,68,4),(329,68,6),(308,68,7),(309,69,1),(170,69,3),(171,69,4),(328,69,6),(172,70,3),(173,70,4),(327,70,6),(310,70,9),(311,71,1),(174,71,3),(175,71,4),(326,71,6),(176,72,3),(177,72,4),(325,72,6),(312,72,7),(178,73,3),(179,73,4),(180,73,6),(181,73,7),(272,74,3),(273,74,4),(274,74,6),(182,74,7),(275,75,3),(276,75,4),(277,75,6),(183,75,7),(278,76,3),(279,76,4),(280,76,6),(184,76,7),(281,77,3),(282,77,4),(283,77,6),(185,77,7),(284,78,3),(285,78,4),(286,78,6),(186,78,7),(287,79,3),(288,79,4),(289,79,6),(187,79,7),(290,81,3),(291,81,4),(292,81,6),(189,81,7),(293,82,3),(294,82,4),(295,82,6),(190,82,7),(296,83,3),(297,83,4),(298,83,6),(191,83,7),(299,84,3),(300,84,4),(301,84,6),(192,84,7),(250,85,3),(251,85,4),(252,85,6),(206,85,7),(253,86,3),(254,86,4),(255,86,6),(207,86,7),(256,87,3),(257,87,4),(258,87,6),(208,87,7),(259,88,3),(260,88,4),(261,88,6),(209,88,7);
/*!40000 ALTER TABLE `control_acero_apoyo_elemento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_archivo`
--

DROP TABLE IF EXISTS `control_acero_archivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_archivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `archivo` longblob NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `etapaAsignacion_id` int(11) DEFAULT NULL,
  `tipo` int(11) NOT NULL,
  `tipoArchivo` varchar(50) DEFAULT NULL,
  `extension` varchar(8),
  `nombreArchivo` varchar(100),
  PRIMARY KEY (`id`),
  KEY `etapaAsignacion_id_69031b8a_fk_control_acero_etapaasignacion_id` (`etapaAsignacion_id`),
  CONSTRAINT `etapaAsignacion_id_69031b8a_fk_control_acero_etapaasignacion_id` FOREIGN KEY (`etapaAsignacion_id`) REFERENCES `control_acero_etapaasignacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_archivo`
--

LOCK TABLES `control_acero_archivo` WRITE;
/*!40000 ALTER TABLE `control_acero_archivo` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_archivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_controlasignacion`
--

DROP TABLE IF EXISTS `control_acero_controlasignacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_controlasignacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad` decimal(20,4),
  `tiempoEntrega` int(11) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `frente_id` int(11) NOT NULL,
  `funcion_id` int(11) NOT NULL,
  `idOrden` int(11),
  `programaSuministro_id` int(11),
  `programaSuministroDetalle_id` int(11),
  PRIMARY KEY (`id`),
  KEY `control_acero_cont_frente_id_1e2599a1_fk_control_acero_frente_id` (`frente_id`),
  KEY `control_acero_co_funcion_id_202d4c2e_fk_control_acero_funcion_id` (`funcion_id`),
  KEY `control_acero_controlasignacion_25010859` (`programaSuministro_id`),
  KEY `control_acero_controlasignacion_fbda3682` (`programaSuministroDetalle_id`),
  CONSTRAINT `D028780a403d95f3e82393aad53423a8` FOREIGN KEY (`programaSuministroDetalle_id`) REFERENCES `control_acero_programasuministrodetalle` (`id`),
  CONSTRAINT `b5a0c37a90ccb5da9d46e83ab43a21c4` FOREIGN KEY (`programaSuministro_id`) REFERENCES `control_acero_programasuministro` (`id`),
  CONSTRAINT `control_acero_co_funcion_id_202d4c2e_fk_control_acero_funcion_id` FOREIGN KEY (`funcion_id`) REFERENCES `control_acero_funcion` (`id`),
  CONSTRAINT `control_acero_cont_frente_id_1e2599a1_fk_control_acero_frente_id` FOREIGN KEY (`frente_id`) REFERENCES `control_acero_frente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_controlasignacion`
--

LOCK TABLES `control_acero_controlasignacion` WRITE;
/*!40000 ALTER TABLE `control_acero_controlasignacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_controlasignacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_despiece`
--

DROP TABLE IF EXISTS `control_acero_despiece`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_despiece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomenclatura` varchar(100) NOT NULL,
  `longitud` double NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `cantidad` int(11) NOT NULL,
  `fechaActualizacion` datetime,
  `figura` varchar(20) NOT NULL,
  `peso` decimal(20,4),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_despiece`
--

LOCK TABLES `control_acero_despiece` WRITE;
/*!40000 ALTER TABLE `control_acero_despiece` DISABLE KEYS */;
INSERT INTO `control_acero_despiece` VALUES (1,'O5C',7.76,1,'2016-05-16 11:09:36',70,'2016-05-16 11:09:36','T1',846.0000),(2,'R5C',7.76,1,'2016-05-16 11:09:36',58,'2016-05-16 11:09:36','T1',701.0000),(3,'P5C',6.54,1,'2016-05-16 11:09:36',70,'2016-05-16 11:09:36','T1',713.0000),(4,'L5C',6.54,1,'2016-05-16 11:09:37',58,'2016-05-16 11:09:37','T1',591.0000),(5,'Q5C',5.66,1,'2016-05-16 11:09:37',70,'2016-05-16 11:09:37','T1',617.0000),(6,'M5C',5.66,1,'2016-05-16 11:09:37',58,'2016-05-16 11:09:37','T1',511.0000),(7,'N5C',1.86,1,'2016-05-16 11:09:37',140,'2016-05-16 11:09:37','YY',405.0000),(8,'W5C',1.16,1,'2016-05-16 11:09:37',48,'2016-05-16 11:09:37','XX',87.0000),(9,'X10C',10.33,1,'2016-05-16 11:09:37',52,'2016-05-16 11:09:37','ZZ',3345.0000),(10,'Y10C',6.54,1,'2016-05-16 11:09:37',50,'2016-05-16 11:09:37','ZZ',2036.0000),(11,'C10C',8.34,1,'2016-05-16 11:09:37',66,'2016-05-16 11:09:37','S15',3428.0000),(12,'A10C',8.25,1,'2016-05-16 11:09:37',66,'2016-05-16 11:09:37','S15',3391.0000),(13,'B10C',8.16,1,'2016-05-16 11:09:37',64,'2016-05-16 11:09:37','S15',3252.0000),(14,'K11C',7.84,1,'2016-05-16 11:09:37',71,'2016-05-16 11:09:37','S15',4175.0000),(15,'D11C',7.75,1,'2016-05-16 11:09:37',71,'2016-05-16 11:09:37','S15',4127.0000),(16,'E10C',8.34,1,'2016-05-16 11:09:37',66,'2016-05-16 11:09:37','S15',3228.0000),(17,'H10C',7.84,1,'2016-05-16 11:09:37',70,'2016-05-16 11:09:37','S15',3417.0000),(18,'G7C',7.87,1,'2016-05-16 11:10:12',19,'2016-05-16 11:10:12','S15',143.0000),(19,'F7C',8.09,1,'2016-05-16 11:10:12',16,'2016-05-16 11:10:12','S15',393.0000),(20,'J7C',7.46,1,'2016-05-16 11:10:13',6,'2016-05-16 11:10:13','S15',136.0000),(21,'I7C',7.59,1,'2016-05-16 11:10:13',16,'2016-05-16 11:10:13','S15',369.0000),(22,'V5C',2.6,1,'2016-05-16 11:10:13',216,'2016-05-16 11:10:13','T12',874.0000),(23,'S5C',2.64,1,'2016-05-16 11:10:13',216,'2016-05-16 11:10:13','T12',888.0000),(24,'T5C',2.74,1,'2016-05-16 11:10:13',216,'2016-05-16 11:10:13','T12',921.0000),(25,'U5C',2.74,1,'2016-05-16 11:10:13',216,'2016-05-16 11:10:13','T12',921.0000);
/*!40000 ALTER TABLE `control_acero_despiece` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_despiece_material`
--

DROP TABLE IF EXISTS `control_acero_despiece_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_despiece_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `despiece_id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `control_acero_despiece_material_despiece_id_900bc3f3_uniq` (`despiece_id`,`material_id`),
  KEY `control_acero__material_id_3648ce15_fk_control_acero_material_id` (`material_id`),
  CONSTRAINT `control_acero__despiece_id_2f5aec96_fk_control_acero_despiece_id` FOREIGN KEY (`despiece_id`) REFERENCES `control_acero_despiece` (`id`),
  CONSTRAINT `control_acero__material_id_3648ce15_fk_control_acero_material_id` FOREIGN KEY (`material_id`) REFERENCES `control_acero_material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_despiece_material`
--

LOCK TABLES `control_acero_despiece_material` WRITE;
/*!40000 ALTER TABLE `control_acero_despiece_material` DISABLE KEYS */;
INSERT INTO `control_acero_despiece_material` VALUES (1,1,5),(2,2,5),(3,3,5),(4,4,5),(5,5,5),(6,6,5),(7,7,5),(8,8,5),(9,9,10),(10,10,10),(11,11,10),(12,12,10),(13,13,10),(14,14,11),(15,15,11),(16,16,10),(17,17,10),(18,18,7),(19,19,7),(20,20,7),(21,21,7),(22,22,5),(23,23,5),(24,24,5),(25,25,5);
/*!40000 ALTER TABLE `control_acero_despiece_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_elemento`
--

DROP TABLE IF EXISTS `control_acero_elemento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_elemento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `peso` double NOT NULL,
  `fechaActualizacion` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_elemento`
--

LOCK TABLES `control_acero_elemento` WRITE;
/*!40000 ALTER TABLE `control_acero_elemento` DISABLE KEYS */;
INSERT INTO `control_acero_elemento` VALUES (1,' Pilas I',' 1',1,'2016-04-29 00:05:41',0,'2016-05-02 16:34:55'),(2,' Zapata I',' 1',1,'2016-04-29 00:08:21',0,'2016-05-02 16:36:26'),(3,' Columnas I',' 1',1,'2016-04-29 00:08:51',0,'2016-05-02 16:13:39'),(4,' Capitel I',' 1',1,'2016-04-29 00:09:37',0,'2016-05-02 16:36:41'),(5,' Pila II',' 2',1,'2016-05-02 16:12:10',0,'2016-05-02 16:12:10'),(6,' Zapata II',' 2',1,'2016-05-02 16:15:13',0,'2016-05-02 16:36:20'),(7,' Pila III',' 3',1,'2016-05-02 16:35:29',0,'2016-05-02 16:35:29'),(8,' Pila IV',' 4',1,'2016-05-02 16:57:17',0,'2016-05-02 16:57:17'),(9,' Pila V',' 5',1,'2016-05-04 16:12:47',0,'2016-05-04 16:12:47');
/*!40000 ALTER TABLE `control_acero_elemento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_elemento_despiece`
--

DROP TABLE IF EXISTS `control_acero_elemento_despiece`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_elemento_despiece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `elemento_id` int(11) NOT NULL,
  `despiece_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `elemento_id` (`elemento_id`,`despiece_id`),
  KEY `control_acero__despiece_id_79617a90_fk_control_acero_despiece_id` (`despiece_id`),
  CONSTRAINT `control_acero__despiece_id_79617a90_fk_control_acero_despiece_id` FOREIGN KEY (`despiece_id`) REFERENCES `control_acero_despiece` (`id`),
  CONSTRAINT `control_acero_e_elemento_id_5cab449_fk_control_acero_elemento_id` FOREIGN KEY (`elemento_id`) REFERENCES `control_acero_elemento` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_elemento_despiece`
--

LOCK TABLES `control_acero_elemento_despiece` WRITE;
/*!40000 ALTER TABLE `control_acero_elemento_despiece` DISABLE KEYS */;
INSERT INTO `control_acero_elemento_despiece` VALUES (26,1,13),(27,1,14),(28,1,15),(29,1,25),(1,2,1),(2,2,2),(3,2,3),(4,2,4),(5,2,5),(6,2,6),(7,2,7),(8,2,8),(9,2,9),(10,2,10),(11,2,11),(12,2,12),(13,2,13),(14,2,14),(15,2,15),(16,2,16),(17,2,17),(18,2,18),(19,2,19),(20,2,20),(21,2,21),(22,2,22),(23,2,23),(24,2,24),(25,2,25),(33,3,2),(34,3,9),(30,3,13),(31,3,20),(32,3,23),(35,4,5),(36,4,7),(38,4,11),(37,4,12),(39,4,25),(44,5,1),(40,5,2),(41,5,13),(43,5,20),(42,5,24),(47,6,5),(48,6,10),(46,6,11),(45,6,13),(50,7,1),(52,7,5),(53,7,8),(51,7,12),(57,8,4),(55,8,6),(56,8,9),(59,8,17),(58,8,25),(65,9,4),(60,9,5),(61,9,6),(62,9,10),(64,9,11),(63,9,25);
/*!40000 ALTER TABLE `control_acero_elemento_despiece` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_elemento_material`
--

DROP TABLE IF EXISTS `control_acero_elemento_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_elemento_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `elemento_id` int(11) NOT NULL,
  `material_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `elemento_id` (`elemento_id`,`material_id`),
  KEY `control_acero__material_id_22763634_fk_control_acero_material_id` (`material_id`),
  CONSTRAINT `control_acero__elemento_id_29328cb0_fk_control_acero_elemento_id` FOREIGN KEY (`elemento_id`) REFERENCES `control_acero_elemento` (`id`),
  CONSTRAINT `control_acero__material_id_22763634_fk_control_acero_material_id` FOREIGN KEY (`material_id`) REFERENCES `control_acero_material` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_elemento_material`
--

LOCK TABLES `control_acero_elemento_material` WRITE;
/*!40000 ALTER TABLE `control_acero_elemento_material` DISABLE KEYS */;
INSERT INTO `control_acero_elemento_material` VALUES (3,1,5),(1,1,8),(2,1,10),(26,1,11),(6,2,5),(7,2,6),(8,2,7),(19,2,10),(20,2,11),(9,3,5),(10,3,6),(13,4,3),(14,4,5),(15,4,6),(11,4,8),(12,4,10),(18,5,5),(16,5,8),(17,5,12),(31,6,3),(23,6,5),(24,6,6),(25,6,7),(30,6,8),(21,6,10),(22,6,11),(29,7,5),(27,7,8),(28,7,10),(33,8,5),(32,8,12),(35,9,5),(34,9,9);
/*!40000 ALTER TABLE `control_acero_elemento_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_etapaasignacion`
--

DROP TABLE IF EXISTS `control_acero_etapaasignacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_etapaasignacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pesoSolicitado` decimal(20,4),
  `pesoRecibido` decimal(20,4),
  `tiempoEntrega` int(11) DEFAULT NULL,
  `cantidadAsignada` decimal(20,4),
  `estatusEtapa` int(11) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `controlAsignacion_id` int(11) NOT NULL,
  `funcion_id` int(11) NOT NULL,
  `taller_id` int(11) DEFAULT NULL,
  `transporte_id` int(11) DEFAULT NULL,
  `programaSuministro_id` int(11),
  `idEtapaPertenece` int(11),
  `piezasRecibidas` int(11),
  `despiece_id` int(11),
  `tipoEstatus` int(11) NOT NULL,
  `tipoRecepcion` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `a66b8f2fc3786bd1aa7fe194de05bdb1` (`controlAsignacion_id`),
  KEY `control_acero_et_funcion_id_5159e4be_fk_control_acero_funcion_id` (`funcion_id`),
  KEY `control_acero_etap_taller_id_21818f8f_fk_control_acero_taller_id` (`taller_id`),
  KEY `control_ac_transporte_id_1f1c8789_fk_control_acero_transporte_id` (`transporte_id`),
  KEY `control_acero_etapaasignacion_25010859` (`programaSuministro_id`),
  KEY `control_acero_etapaasignacion_e3c75c4a` (`despiece_id`),
  CONSTRAINT `a66b8f2fc3786bd1aa7fe194de05bdb1` FOREIGN KEY (`controlAsignacion_id`) REFERENCES `control_acero_controlasignacion` (`id`),
  CONSTRAINT `control_ac_transporte_id_1f1c8789_fk_control_acero_transporte_id` FOREIGN KEY (`transporte_id`) REFERENCES `control_acero_transporte` (`id`),
  CONSTRAINT `control_acero__despiece_id_29861cd9_fk_control_acero_despiece_id` FOREIGN KEY (`despiece_id`) REFERENCES `control_acero_despiece` (`id`),
  CONSTRAINT `control_acero_et_funcion_id_5159e4be_fk_control_acero_funcion_id` FOREIGN KEY (`funcion_id`) REFERENCES `control_acero_funcion` (`id`),
  CONSTRAINT `control_acero_etap_taller_id_21818f8f_fk_control_acero_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `control_acero_taller` (`id`),
  CONSTRAINT `e399b88ce4803ea5d8c6e9a9c95e5744` FOREIGN KEY (`programaSuministro_id`) REFERENCES `control_acero_programasuministro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_etapaasignacion`
--

LOCK TABLES `control_acero_etapaasignacion` WRITE;
/*!40000 ALTER TABLE `control_acero_etapaasignacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_etapaasignacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_factor`
--

DROP TABLE IF EXISTS `control_acero_factor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_factor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pva` int(11) NOT NULL,
  `factorPulgada` decimal(20,4) DEFAULT NULL,
  `pi` decimal(20,4) DEFAULT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime DEFAULT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_factor`
--

LOCK TABLES `control_acero_factor` WRITE;
/*!40000 ALTER TABLE `control_acero_factor` DISABLE KEYS */;
INSERT INTO `control_acero_factor` VALUES (1,7857,25.4000,3.1415,1,'2016-05-12 17:25:04','2016-05-12 17:25:04');
/*!40000 ALTER TABLE `control_acero_factor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_frente`
--

DROP TABLE IF EXISTS `control_acero_frente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_frente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `identificacion` varchar(100) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `kilometros` double NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_frente`
--

LOCK TABLES `control_acero_frente` WRITE;
/*!40000 ALTER TABLE `control_acero_frente` DISABLE KEYS */;
INSERT INTO `control_acero_frente` VALUES (1,'Viaducto 1E','Zinacantepec-Marqueza','Mexico-Toluca',2,1,'2016-05-16 11:30:18'),(2,'Viaducto 1C','Marqueza','Mexico-Toluca',3,1,'2016-05-16 11:30:18'),(3,'Viaducto 1D','Marqueza','Mexico-Toluca',4,1,'2016-05-16 11:30:19'),(4,'Viaducto 1B','Zinancantepec','Mexico-Toluca',5,1,'2016-05-16 11:30:19'),(5,'Estacion Metepec','Metepec','Mexico-Toluca',6,1,'2016-05-16 11:30:19'),(6,'Estacion Lerma','Lerma','Mexico-Toluca',7,1,'2016-05-16 11:30:19');
/*!40000 ALTER TABLE `control_acero_frente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_funcion`
--

DROP TABLE IF EXISTS `control_acero_funcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_funcion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` int(11) NOT NULL,
  `proveedor` varchar(20) NOT NULL,
  `tonelajeMaximo` double NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_funcion`
--

LOCK TABLES `control_acero_funcion` WRITE;
/*!40000 ALTER TABLE `control_acero_funcion` DISABLE KEYS */;
INSERT INTO `control_acero_funcion` VALUES (1,1,'DEACERO',0,1,'2016-04-28 23:24:00'),(2,1,'ARCELORMITTAL',0,1,'2016-04-28 23:24:46'),(3,1,'CORSA',0,1,'2016-04-28 23:25:15'),(4,1,'TYASA',0,1,'2016-04-28 23:25:32'),(5,2,'SMC',0,1,'2016-04-28 23:26:01'),(6,2,'COREMAN',0,1,'2016-04-28 23:26:26'),(7,2,'COLLADO',0,1,'2016-04-28 23:26:41'),(8,2,'FONTANA',0,1,'2016-04-28 23:32:47'),(9,2,'CORAS',0,1,'2016-04-28 23:36:39'),(10,1,'LA PENINSULAR',0,1,'2016-04-28 23:36:57'),(17,3,'FONTANA',0,1,'2016-05-02 18:01:30'),(18,3,'CORSA',0,1,'2016-05-02 18:01:37'),(19,3,'TYASA',0,1,'2016-05-02 18:01:44'),(20,4,'SMC',0,1,'2016-05-02 18:01:51'),(21,4,'COLLADO',0,1,'2016-05-02 18:01:54'),(22,4,'LA PENINSULAR',0,1,'2016-05-02 18:01:59');
/*!40000 ALTER TABLE `control_acero_funcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_grupo`
--

DROP TABLE IF EXISTS `control_acero_grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_grupo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_grupo`
--

LOCK TABLES `control_acero_grupo` WRITE;
/*!40000 ALTER TABLE `control_acero_grupo` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_material`
--

DROP TABLE IF EXISTS `control_acero_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_material` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `diametro` decimal(20,4),
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `peso` decimal(20,4) DEFAULT NULL,
  `proveedor` varchar(20) NOT NULL,
  `tipo` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `numero` int(11) NOT NULL,
  `longitud` int(11) DEFAULT NULL,
  `factor_id` int(11),
  PRIMARY KEY (`id`),
  KEY `control_acero_material_faccef0b` (`factor_id`),
  CONSTRAINT `control_acero_mate_factor_id_4b00512b_fk_control_acero_factor_id` FOREIGN KEY (`factor_id`) REFERENCES `control_acero_factor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_material`
--

LOCK TABLES `control_acero_material` WRITE;
/*!40000 ALTER TABLE `control_acero_material` DISABLE KEYS */;
INSERT INTO `control_acero_material` VALUES (1,9.5250,1,'2016-05-13 11:07:54',0.5598,'DEACERO',1,'Varilla #3',3,12,1),(3,12.7000,1,'2016-05-13 11:07:54',0.9953,'DEACERO',1,'Varilla #4',4,12,1),(5,15.8750,1,'2016-05-13 11:07:54',1.5551,'DEACERO',1,'Varilla #5',5,12,1),(6,19.0500,1,'2016-05-13 11:07:54',2.2394,'DEACERO',2,'Varilla #6',6,12,1),(7,22.2250,1,'2016-05-13 11:07:54',3.0480,'DEACERO',1,'Varilla #7',7,12,1),(8,25.4000,1,'2016-05-13 11:07:54',3.9811,'DEACERO',1,'Varilla #8',8,12,1),(9,28.5750,1,'2016-05-13 11:07:54',5.0386,'DEACERO',1,'Varilla #9',9,12,1),(10,31.7500,1,'2016-05-13 11:07:54',6.2205,'DEACERO',1,'Varilla #10',10,12,1),(11,34.9250,1,'2016-05-13 11:07:54',7.5268,'DEACERO',1,'Varilla #11',11,12,1),(12,38.1000,1,'2016-05-13 11:07:54',8.9575,'DEACERO',1,'Varilla #12',12,12,1);
/*!40000 ALTER TABLE `control_acero_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_modulo`
--

DROP TABLE IF EXISTS `control_acero_modulo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_modulo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `padre` int(11) NOT NULL,
  `url` varchar(100) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_modulo`
--

LOCK TABLES `control_acero_modulo` WRITE;
/*!40000 ALTER TABLE `control_acero_modulo` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_modulo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_programasuministro`
--

DROP TABLE IF EXISTS `control_acero_programasuministro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_programasuministro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idOrden` int(11) NOT NULL,
  `fechaInicial` date NOT NULL,
  `fechaFinal` date NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `frente_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `control_acero_prog_frente_id_3d740b3b_fk_control_acero_frente_id` (`frente_id`),
  CONSTRAINT `control_acero_prog_frente_id_3d740b3b_fk_control_acero_frente_id` FOREIGN KEY (`frente_id`) REFERENCES `control_acero_frente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_programasuministro`
--

LOCK TABLES `control_acero_programasuministro` WRITE;
/*!40000 ALTER TABLE `control_acero_programasuministro` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_programasuministro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_programasuministrodetalle`
--

DROP TABLE IF EXISTS `control_acero_programasuministrodetalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_programasuministrodetalle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `peso` decimal(20,4) DEFAULT NULL,
  `estatus` int(11) NOT NULL,
  `fechaActualizacion` datetime NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `apoyo_id` int(11) NOT NULL,
  `elemento_id` int(11) NOT NULL,
  `cantidad` int(11),
  `material_id` int(11),
  `programaSuministro_id` int(11),
  PRIMARY KEY (`id`),
  KEY `control_acero_progra_apoyo_id_68f293c8_fk_control_acero_apoyo_id` (`apoyo_id`),
  KEY `control_acero__elemento_id_36a836ec_fk_control_acero_elemento_id` (`elemento_id`),
  KEY `control_acero_programasuministrodetalle_eb4b9aaa` (`material_id`),
  KEY `control_acero_programasuministrodetalle_25010859` (`programaSuministro_id`),
  CONSTRAINT `control_acero__elemento_id_36a836ec_fk_control_acero_elemento_id` FOREIGN KEY (`elemento_id`) REFERENCES `control_acero_elemento` (`id`),
  CONSTRAINT `control_acero_pr_material_id_836628_fk_control_acero_material_id` FOREIGN KEY (`material_id`) REFERENCES `control_acero_material` (`id`),
  CONSTRAINT `control_acero_progra_apoyo_id_68f293c8_fk_control_acero_apoyo_id` FOREIGN KEY (`apoyo_id`) REFERENCES `control_acero_apoyo` (`id`),
  CONSTRAINT `d42b1202a575820bf956080a5bf04744` FOREIGN KEY (`programaSuministro_id`) REFERENCES `control_acero_programasuministro` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_programasuministrodetalle`
--

LOCK TABLES `control_acero_programasuministrodetalle` WRITE;
/*!40000 ALTER TABLE `control_acero_programasuministrodetalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `control_acero_programasuministrodetalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_taller`
--

DROP TABLE IF EXISTS `control_acero_taller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `proveedor` varchar(20) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  `responsable` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_taller`
--

LOCK TABLES `control_acero_taller` WRITE;
/*!40000 ALTER TABLE `control_acero_taller` DISABLE KEYS */;
INSERT INTO `control_acero_taller` VALUES (1,'Taller de Habilitado de Toluca','Test1','Tollocan 1',1,'2016-05-02 18:07:01','Jose Gonzalez Martinez'),(2,'Talle de Habilitado Tollocan','Test2','Paseo Tollocan',1,'2016-05-02 18:07:36','Angela Rodriguez');
/*!40000 ALTER TABLE `control_acero_taller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `control_acero_transporte`
--

DROP TABLE IF EXISTS `control_acero_transporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `control_acero_transporte` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` int(11) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `placas` varchar(20) NOT NULL,
  `estatus` int(11) NOT NULL,
  `fechaRegistro` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `control_acero_transporte`
--

LOCK TABLES `control_acero_transporte` WRITE;
/*!40000 ALTER TABLE `control_acero_transporte` DISABLE KEYS */;
INSERT INTO `control_acero_transporte` VALUES (2,1,20000,'XHQ900',1,'2016-05-02 18:19:46'),(3,1,3000,'WERTYQ',1,'2016-05-02 18:20:04'),(4,1,10000,'TYUIO',1,'2016-05-02 18:20:15'),(5,1,40000,'543TGS',1,'2016-05-02 18:20:27');
/*!40000 ALTER TABLE `control_acero_transporte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-04-18 19:36:06','1','VARILLA DE PRUEBA',1,'Añadido.',7,1),(2,'2016-04-18 19:36:18','2','Otro tal',1,'Añadido.',7,1),(3,'2016-04-18 19:52:13','3','otras 2 varillas',1,'Añadido.',7,1),(4,'2016-04-18 19:52:30','1','Despiece 1',1,'Añadido.',8,1),(5,'2016-04-18 20:01:32','1','Despiece 1',3,'',8,1),(6,'2016-04-18 20:02:18','2','despiece tal',1,'Añadido.',8,1),(7,'2016-04-18 20:02:44','2','despiece tal',2,'Modificado/a material.',8,1),(8,'2016-04-18 20:06:25','1','pared frontal',1,'Añadido.',9,1),(9,'2016-04-18 20:25:31','2','despiece tal',2,'Modificado/a material.',8,1),(10,'2016-04-18 20:25:38','2','despiece tal',2,'No ha cambiado ningún campo.',8,1),(11,'2016-04-18 20:26:17','1','Capitel Parte Frontal',2,'Modificado/a nombre, longitud, alto y ancho.',9,1),(12,'2016-04-18 20:26:41','2','Capitel Parte Trasera',1,'Añadido.',9,1),(14,'2016-04-18 21:58:18','3','despiece nuevo',1,'Añadido.',8,1),(15,'2016-04-18 21:58:22','3','parte frontal de la pila',1,'Añadido.',9,1),(17,'2016-04-19 14:13:29','1','VARILLA DE PRUEBA',1,'Añadido.',7,1),(18,'2016-04-19 19:24:12','1','otro',1,'Añadido.',8,1),(19,'2016-04-19 19:35:09','2','despiece prueba',1,'Añadido.',8,1),(20,'2016-04-19 19:35:18','1','elemento prueba',1,'Añadido.',9,1),(22,'2016-04-22 05:56:36','1','frente de prueba',1,'',15,2),(23,'2016-04-22 14:44:07','1','Aceros Mexicanos',1,'',14,2),(24,'2016-04-22 15:29:36','2','Alumex Toluca',1,'',14,2),(25,'2016-04-22 18:22:06','2','Frente de Trabajo Inicial',1,'',15,2),(26,'2016-04-22 18:32:57','2','Varilla normal',1,'',7,2),(27,'2016-04-22 18:33:27','3','Varilla Especial',1,'',7,2),(28,'2016-04-22 18:33:30','3','despiece 1',1,'',8,2),(29,'2016-04-22 18:33:53','4','despiece normal',1,'',8,2),(30,'2016-04-22 18:33:58','2','pila1',1,'',9,2),(33,'2016-04-22 20:53:30','2','despiece prueba',2,'Modificado/a material.',8,2),(34,'2016-04-27 21:52:54','3','moises.rosas',1,'',4,2),(35,'2016-04-27 23:33:35','3','moises.rosas',2,'Modificado/a user_permissions.',4,2),(36,'2016-04-27 23:34:21','4','prueba',1,'',4,2),(37,'2016-04-27 23:34:42','4','prueba',2,'Modificado/a user_permissions.',4,2),(38,'2016-04-27 23:35:23','4','prueba',2,'Modificado/a is_staff.',4,2),(39,'2016-04-28 15:48:25','3','moises.rosas',3,'',4,2),(40,'2016-04-28 23:32:41','1','asdf',1,'',7,2),(41,'2016-04-28 23:32:45','1','test',1,'',9,2),(42,'2016-04-29 15:23:18','1','Viaducto 1E',1,'',15,2),(43,'2016-04-29 15:58:16','1','Viaducto 1E',2,'Modificado/a identificacion.',15,2),(44,'2016-04-29 16:30:13','1','Viaducto 1E',1,'',15,2),(45,'2016-04-29 16:58:42','1','Varilla #3',2,'Modificado/a numero.',7,2),(46,'2016-04-29 16:58:46','3','Varilla #4',2,'Modificado/a numero.',7,2),(47,'2016-04-29 16:58:50','5','Varilla #5',2,'Modificado/a numero.',7,2),(48,'2016-04-29 16:58:54','6','Varilla #6',2,'Modificado/a numero.',7,2),(49,'2016-04-29 16:59:01','7','Varilla #7',2,'Modificado/a numero.',7,2),(50,'2016-04-29 16:59:06','8','Varilla #8',2,'Modificado/a numero.',7,2),(51,'2016-04-29 16:59:10','9','Varilla #9',2,'Modificado/a numero.',7,2),(52,'2016-04-29 16:59:16','10','Varilla #10',2,'Modificado/a numero.',7,2),(53,'2016-04-29 16:59:20','11','Varilla #11',2,'Modificado/a numero.',7,2),(54,'2016-04-29 16:59:25','12','Varilla #12',2,'Modificado/a numero.',7,2),(55,'2016-05-02 17:13:46','11','Armado 1',1,'',14,2),(56,'2016-05-02 17:13:52','12','Armado 2',1,'',14,2),(57,'2016-05-02 17:13:57','13','Armado 3',1,'',14,2),(58,'2016-05-02 17:14:16','14','Colocador 1',1,'',14,2),(59,'2016-05-02 17:14:23','15','Colocador 2',1,'',14,2),(60,'2016-05-02 17:14:32','16','Colocador 3',1,'',14,2),(61,'2016-05-02 18:01:30','17','Armado 1',1,'',14,2),(62,'2016-05-02 18:01:37','18','Armado 2',1,'',14,2),(63,'2016-05-02 18:01:44','19','Armado 3',1,'',14,2),(64,'2016-05-02 18:01:51','20','Colocador 1',1,'',14,2),(65,'2016-05-02 18:01:54','21','Colocador 2',1,'',14,2),(66,'2016-05-02 18:01:59','22','Colocador 3',1,'',14,2),(67,'2016-05-02 18:02:39','20','Colocador 1',2,'No ha cambiado ningún campo.',14,2),(68,'2016-05-02 18:02:45','21','Colocador 2',2,'No ha cambiado ningún campo.',14,2),(69,'2016-05-02 18:02:50','22','Colocador 3',2,'No ha cambiado ningún campo.',14,2),(70,'2016-05-02 18:03:26','20','Colocador 1',2,'No ha cambiado ningún campo.',14,2),(71,'2016-05-02 18:03:31','20','Colocador 1',2,'No ha cambiado ningún campo.',14,2),(72,'2016-05-02 18:03:36','20','Colocador 1',2,'No ha cambiado ningún campo.',14,2),(73,'2016-05-02 18:04:22','20','Colocador 1',2,'Modificado/a tipo.',14,2),(74,'2016-05-02 18:04:26','21','Colocador 2',2,'Modificado/a tipo.',14,2),(75,'2016-05-02 18:04:32','22','Colocador 3',2,'Modificado/a tipo.',14,2),(76,'2016-05-02 18:07:01','1','Taller de Habilitado de Toluca',1,'',13,2),(77,'2016-05-02 18:07:36','2','Talle de Habilitado Tollocan',1,'',13,2),(78,'2016-05-02 18:19:46','2','XHQ900',1,'',12,2),(79,'2016-05-02 18:20:04','3','WERTYQ',1,'',12,2),(80,'2016-05-02 18:20:15','4','TYUIO',1,'',12,2),(81,'2016-05-02 18:20:27','5','543TGS',1,'',12,2),(82,'2016-05-03 17:04:16','13','material de Prueba',1,'',7,2),(83,'2016-05-03 17:04:28','13','material de Prueba',3,'',7,2),(84,'2016-05-04 15:18:15','1','despiece 1',1,'',8,2),(85,'2016-05-04 15:18:46','5','elemento prueba',1,'',9,2),(86,'2016-05-04 15:19:08','5','elemento prueba',3,'',9,2),(87,'2016-05-04 15:46:35','1','despiece 1',3,'',8,2),(88,'2016-05-04 15:53:08','2','05C',1,'',8,2),(89,'2016-05-04 15:54:11','3','R5C',1,'',8,2),(90,'2016-05-04 15:55:31','4','P5C',1,'',8,2),(91,'2016-05-04 15:56:21','5','L5C',1,'',8,2),(92,'2016-05-04 15:56:26','1','Pilas I',2,'Modificado/a despiece.',9,2),(93,'2016-05-04 23:43:25','5','dbenitezc',1,'',4,2),(94,'2016-05-04 23:43:33','5','dbenitezc',2,'Modificado/a is_staff.',4,2),(95,'2016-05-04 23:46:31','5','dbenitezc',2,'Modificado/a is_superuser.',4,2),(96,'2016-05-12 17:25:04','1','1',1,'',28,5),(97,'2016-05-12 23:22:00','6','test',1,'',4,5);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(19,'control_acero','apoyo'),(26,'control_acero','archivo'),(16,'control_acero','controlasignacion'),(8,'control_acero','despiece'),(9,'control_acero','elemento'),(23,'control_acero','etapaasignacion'),(28,'control_acero','factor'),(15,'control_acero','frente'),(14,'control_acero','funcion'),(25,'control_acero','grupo'),(7,'control_acero','material'),(24,'control_acero','modulo'),(21,'control_acero','programasuministro'),(22,'control_acero','programasuministrodetalle'),(13,'control_acero','taller'),(12,'control_acero','transporte'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-04-18 16:43:11'),(2,'auth','0001_initial','2016-04-18 16:43:25'),(3,'admin','0001_initial','2016-04-18 16:43:27'),(4,'admin','0002_logentry_remove_auto_add','2016-04-18 16:43:27'),(5,'contenttypes','0002_remove_content_type_name','2016-04-18 16:43:29'),(6,'auth','0002_alter_permission_name_max_length','2016-04-18 16:43:30'),(7,'auth','0003_alter_user_email_max_length','2016-04-18 16:43:32'),(8,'auth','0004_alter_user_username_opts','2016-04-18 16:43:32'),(9,'auth','0005_alter_user_last_login_null','2016-04-18 16:43:33'),(10,'auth','0006_require_contenttypes_0002','2016-04-18 16:43:33'),(11,'auth','0007_alter_validators_add_error_messages','2016-04-18 16:43:33'),(12,'sessions','0001_initial','2016-04-18 16:43:34'),(13,'control_acero','0001_initial','2016-04-18 17:19:13'),(14,'control_acero','0002_auto_20160418_1224','2016-04-18 17:25:19'),(15,'control_acero','0003_auto_20160418_1228','2016-04-18 17:28:19'),(16,'control_acero','0004_auto_20160418_1234','2016-04-18 17:34:19'),(17,'control_acero','0005_auto_20160418_1239','2016-04-18 17:39:21'),(18,'control_acero','0006_auto_20160418_1242','2016-04-18 17:43:15'),(19,'control_acero','0007_auto_20160418_1248','2016-04-18 17:48:24'),(20,'control_acero','0008_auto_20160418_1251','2016-04-18 17:51:27'),(21,'control_acero','0009_auto_20160418_1257','2016-04-18 17:57:29'),(22,'control_acero','0010_auto_20160418_1258','2016-04-18 17:58:50'),(23,'control_acero','0011_auto_20160418_1312','2016-04-18 18:13:04'),(24,'control_acero','0012_auto_20160418_1326','2016-04-18 19:25:38'),(25,'control_acero','0013_auto_20160418_1327','2016-04-18 19:25:38'),(26,'control_acero','0014_auto_20160418_1328','2016-04-18 19:25:38'),(27,'control_acero','0015_auto_20160418_1329','2016-04-18 19:25:38'),(28,'control_acero','0016_auto_20160418_1334','2016-04-18 19:25:38'),(29,'control_acero','0017_auto_20160418_1415','2016-04-18 19:25:38'),(30,'control_acero','0018_auto_20160418_1418','2016-04-18 19:25:38'),(31,'control_acero','0019_despiece_material','2016-04-18 19:34:51'),(32,'control_acero','0020_auto_20160418_1442','2016-04-18 19:42:36'),(33,'control_acero','0021_auto_20160418_1450','2016-04-18 19:51:37'),(34,'control_acero','0022_auto_20160418_1505','2016-04-18 20:05:36'),(35,'control_acero','0023_auto_20160418_1709','2016-04-18 22:09:26'),(36,'control_acero','0024_auto_20160418_1745','2016-04-18 22:46:14'),(37,'control_acero','0025_auto_20160420_1101','2016-04-20 16:02:32'),(38,'control_acero','0026_controlasignacion','2016-04-22 16:07:54'),(39,'control_acero','0027_remove_controlasignacion_nombre','2016-04-22 16:09:44'),(40,'control_acero','0028_asignacionetapa','2016-04-22 16:28:51'),(41,'control_acero','0029_frenteasigna','2016-04-25 20:05:41'),(42,'control_acero','0030_auto_20160427_1353','2016-04-27 18:54:37'),(43,'control_acero','0031_auto_20160427_1408','2016-04-27 19:08:54'),(44,'control_acero','0032_auto_20160427_1428','2016-04-27 19:28:59'),(45,'control_acero','0033_remove_frente_estatusfrente','2016-04-27 19:32:30'),(46,'control_acero','0034_material_nombre','2016-04-28 21:52:06'),(47,'control_acero','0035_auto_20160429_1021','2016-04-29 15:21:56'),(48,'control_acero','0036_material_numero','2016-04-29 16:58:30'),(49,'control_acero','0037_programasuministro','2016-04-29 18:42:03'),(50,'control_acero','0038_delete_programasuministro','2016-04-29 19:03:20'),(51,'control_acero','0039_programasuministro_programasuministrodetalle','2016-04-29 19:39:54'),(52,'control_acero','0037_programasuministro_programasuministrodetalle','2016-04-29 19:55:44'),(53,'control_acero','0038_controlasignacion_idprogramasuministro','2016-04-29 21:07:12'),(54,'control_acero','0039_controlasignacion_idorden','2016-04-29 21:31:38'),(55,'control_acero','0040_controlasignacion_elemento','2016-05-01 17:15:06'),(56,'control_acero','0041_auto_20160501_1225','2016-05-01 17:25:44'),(57,'control_acero','0042_auto_20160501_1248','2016-05-01 17:48:45'),(58,'control_acero','0043_auto_20160501_1356','2016-05-01 18:56:59'),(59,'control_acero','0044_auto_20160501_1509','2016-05-01 20:09:22'),(60,'control_acero','0045_etapaasignacion','2016-05-01 20:25:25'),(61,'control_acero','0046_auto_20160502_1041','2016-05-02 15:41:40'),(62,'control_acero','0047_auto_20160502_1044','2016-05-02 15:44:25'),(63,'control_acero','0048_auto_20160502_1052','2016-05-02 15:52:32'),(64,'control_acero','0049_auto_20160502_1053','2016-05-02 15:53:32'),(65,'control_acero','0050_etapaasignacion_programasuministro','2016-05-02 16:35:25'),(66,'control_acero','0051_auto_20160502_1304','2016-05-02 18:04:14'),(67,'control_acero','0052_auto_20160502_1318','2016-05-02 18:18:51'),(68,'control_acero','0053_etapaasignacion_idetapapertenece','2016-05-02 19:52:05'),(69,'control_acero','0054_auto_20160503_1147','2016-05-03 16:47:27'),(70,'control_acero','0055_auto_20160503_1152','2016-05-03 16:52:22'),(71,'control_acero','0056_auto_20160503_1203','2016-05-03 17:03:26'),(72,'control_acero','0057_auto_20160503_1207','2016-05-03 17:07:23'),(73,'control_acero','0058_auto_20160503_1307','2016-05-03 18:07:31'),(74,'control_acero','0059_auto_20160503_1309','2016-05-03 18:09:29'),(75,'control_acero','0060_elemento_despiece','2016-05-04 15:17:25'),(76,'control_acero','0061_auto_20160504_1049','2016-05-04 15:49:49'),(77,'control_acero','0062_etapaasignacion_piezasrecibidas','2016-05-04 17:05:22'),(78,'control_acero','0063_etapaasignacion_despiece','2016-05-04 19:45:24'),(79,'control_acero','0064_etapaasignacion_tipoestatus','2016-05-05 22:18:55'),(80,'control_acero','0065_auto_20160505_1719','2016-05-05 22:19:38'),(81,'control_acero','0066_auto_20160505_1810','2016-05-05 23:10:26'),(82,'control_acero','0067_modulo','2016-05-06 18:58:47'),(83,'control_acero','0068_auto_20160509_1403','2016-05-09 19:04:26'),(84,'control_acero','0069_archivo','2016-05-11 20:19:52'),(85,'control_acero','0070_archivo_tipo','2016-05-11 20:34:29'),(86,'control_acero','0071_archivo_typoarchivo','2016-05-12 02:01:14'),(87,'control_acero','0072_auto_20160511_2130','2016-05-12 02:30:57'),(88,'control_acero','0073_material_longitud','2016-05-12 15:19:48'),(89,'control_acero','0074_auto_20160512_1134','2016-05-12 16:34:18'),(90,'control_acero','0075_auto_20160512_1202','2016-05-12 17:02:47'),(91,'control_acero','0076_factores','2016-05-12 17:19:27'),(92,'control_acero','0077_auto_20160512_1221','2016-05-12 17:21:41'),(93,'control_acero','0078_auto_20160512_1432','2016-05-12 19:32:44'),(94,'control_acero','0079_delete_ingenieria','2016-05-16 15:10:17'),(95,'control_acero','0080_delete_frenteasigna','2016-05-16 15:21:20'),(96,'control_acero','0081_auto_20160516_1056','2016-05-16 15:56:55');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('712br99nbhv79sb3dgh3q9nppu3rx90b','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:00:51'),('8d68w8j8bw998hjznij5nfkqyaheoih3','M2JmMDM5MTExMzQxMzJmM2IxZjg5MWY0OGJmOGJmOWJiOGE0OWRjNzp7Il9hdXRoX3VzZXJfaGFzaCI6ImM1YWZmMDI1MzczMTlmMzliYjdlMDQ0NTE0YTU1MDk0OGM3ZjJjMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-04 14:23:07'),('cv9lz5y4tcepj9ihvybkrkiud1c42gki','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:00:52'),('e42wcjt08z85t072xj7tohfrvon0xdjs','NjU0MTcxMzkzNmNiMGFlMjA0ZjhhNTNiOTMzMTYwYWI3MDdlYTU4ZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjU5ZmU5YWE0YWQ5MDMyY2JmYWM0ZjE5ODY4ZGMwYzM2ZjQwZDIwNGEiLCJjbGF2ZSI6IlJqMW0zbjN6IiwiX2F1dGhfdXNlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsInVzdWFyaW8iOiJyb21hbi5qaW1lbmV6LmVzdHJhZGEifQ==','2016-05-09 15:28:59'),('gj4y828lxlh4rtmjkn9rjbv8dxc8vm6k','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:00:52'),('le0i0piwgyan6xac88qnf62zbtpqn2ah','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:35:03'),('lx4v4of4hghd3u3we7qzcpv8o6wnd82r','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:35:03'),('qrk40kvhlfqxh1bfqbffbcbcwhimhfwd','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:35:02'),('s2h1jonh8kbcm77o91ow1kn6xpvzzfta','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:35:03'),('ude61xlku72xhdsbo5674yoer55k640a','MGFjYWUxNjBjMDcwNTFkYjYwNGNkYzcxYzYwMjc0ZjlmNjZiOTZmMjp7Il9hdXRoX3VzZXJfaWQiOiI1IiwidXN1YXJpbyI6InJvbWFuLmppbWVuZXouZXN0cmFkYSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiaWR1c3VhcmlvIjozMTgxLCJjbGF2ZSI6IlJqMW0zbjN6IiwiX2F1dGhfdXNlcl9oYXNoIjoiNTUwOTAzZWYxY2M4OTlmYWVjNDkxZjM5M2U4NmE3YTRlYjVjNjQ2OCJ9','2016-05-30 15:04:01'),('za7f7y664ax2rcrmpaq4u8d8ih0izoge','YjlmMjY4MzQzMGI2ZjM3YjM1ZWI4ODdlYjY5NmUyNjJmMjVkZDFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjY2MmJmZjRkYzY0MTVmNzBmOTE1MGQ5YmQ4N2JhNDBmZTA0MjYxMmEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-03 15:00:51');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-16 14:53:28
