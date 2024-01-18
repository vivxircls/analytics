-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: shops_insights
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bombayshavinginsights`
--

DROP TABLE IF EXISTS `bombayshavinginsights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bombayshavinginsights` (
  `date` date NOT NULL,
  `datacount_for_customers` float DEFAULT NULL,
  `datacount` float DEFAULT NULL,
  `total_quantity` float DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  `total_order` float DEFAULT NULL,
  `total_return_quantity` float DEFAULT NULL,
  `return_rate` float DEFAULT NULL,
  `average_order_value` float DEFAULT NULL,
  `average_units_ordered` float DEFAULT NULL,
  `return_customer_rate` float DEFAULT NULL,
  `unique_users` varchar(45) DEFAULT NULL,
  KEY `date_index` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bombayshavinginsights`
--

LOCK TABLES `bombayshavinginsights` WRITE;
/*!40000 ALTER TABLE `bombayshavinginsights` DISABLE KEYS */;
INSERT INTO `bombayshavinginsights` VALUES ('2024-01-16',548,822,2778,599841,822,93,3.35,729.73,3.38,4.72,'784');
/*!40000 ALTER TABLE `bombayshavinginsights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bombayshavingtop_channels`
--

DROP TABLE IF EXISTS `bombayshavingtop_channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bombayshavingtop_channels` (
  `date` date NOT NULL,
  `channel_name` varchar(100) DEFAULT NULL,
  `sold_quantity` int DEFAULT NULL,
  KEY `date_index` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bombayshavingtop_channels`
--

LOCK TABLES `bombayshavingtop_channels` WRITE;
/*!40000 ALTER TABLE `bombayshavingtop_channels` DISABLE KEYS */;
INSERT INTO `bombayshavingtop_channels` VALUES ('2024-01-16','Not available',808),('2024-01-16','Applbrew Plus',11),('2024-01-16','Online Store',3);
/*!40000 ALTER TABLE `bombayshavingtop_channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bombayshavingtop_products`
--

DROP TABLE IF EXISTS `bombayshavingtop_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bombayshavingtop_products` (
  `date` date DEFAULT NULL,
  `name` varchar(300) NOT NULL,
  `quantity` int DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  KEY `index1` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bombayshavingtop_products`
--

LOCK TABLES `bombayshavingtop_products` WRITE;
/*!40000 ALTER TABLE `bombayshavingtop_products` DISABLE KEYS */;
INSERT INTO `bombayshavingtop_products` VALUES ('2024-01-16','5 in 1 Brightening Cream',24,5880),('2024-01-16','5 in 1 Brightening Cream-',1,199),('2024-01-16','6-in-1 Premium Shaving Kit For Men',2,6250),('2024-01-16','6-in-1 Sensi Luxe Shaving Kit',10,19990),('2024-01-16','Anti Acne Face Wash, 150g',31,10819),('2024-01-16','Anti Redness Shave Gel, 100g',7,1575),('2024-01-16','Aqua Body Spray, 150ml',12,4788),('2024-01-16','Bearberry Body Yogurt',3,1485),('2024-01-16','Beard Comb Pocket Size',1,295),('2024-01-16','Beard Oil Cedarwood 30ml',28,9100),('2024-01-16','Beard Shaper Tool',34,10166),('2024-01-16','Beard Softener, 45gm',15,4425),('2024-01-16','Black Metal Precision Safety Razor for Men',2,3990),('2024-01-16','Black Vibe Deo For Men, 150ml',77,27335),('2024-01-16','Black Vibe Deo For Men, 150ml-',1,249),('2024-01-16','Cairo, 100ml',20,15900),('2024-01-16','Cairo, 100ml-',1,599),('2024-01-16','Challenger Razor (Pack Of 10)',25,6250),('2024-01-16','Challenger Razor (Pack Of 5) & Shaving Gel Combo-',1,249),('2024-01-16','Charcoal Bath Soap',4,500),('2024-01-16','Charcoal Bath Soap, 100g',1,125),('2024-01-16','Charcoal Bath Soap, 100g (Pack of 3)',47,16215),('2024-01-16','Charcoal Face Care Kit',2,1572),('2024-01-16','Charcoal Face Care Kit with Sheet Mask',1,799),('2024-01-16','Charcoal Face Pack - 50g',2,558),('2024-01-16','Charcoal Face Pack, 100g',6,1914),('2024-01-16','Charcoal Face Pack, 50g',9,2511),('2024-01-16','Charcoal Face Scrub, 100g',21,6279),('2024-01-16','Charcoal Face Scrub, 45g-45gm',1,99),('2024-01-16','Charcoal Face Sheet Mask (Pack of 2)',14,4172),('2024-01-16','Charcoal Face Wash & Coffee Face Wash Combo-',1,299),('2024-01-16','Charcoal Face Wash & Peel Off Combo',1,608),('2024-01-16','Charcoal Face Wash, 100g',31,8029),('2024-01-16','Charcoal Face Wash, 100g-',3,597),('2024-01-16','Charcoal Face Wash, 50g (Pack of 2)',1,198),('2024-01-16','Charcoal Hair Removal Spray, 200ml',36,17964),('2024-01-16','Charcoal Peel Off Mask, 100g',23,7337),('2024-01-16','Charcoal Peel Off Mask, 60g',1,199),('2024-01-16','Charcoal Peel Off Mask, 60g-60 GM',1,99),('2024-01-16','Charcoal Shaving Cream, 78g',8,792),('2024-01-16','Charcoal Shaving Foam, 425g',32,8800),('2024-01-16','Charcoal Shaving Foam, 425g-',2,498),('2024-01-16','Charcoal Shaving Foam, 50g',2,190),('2024-01-16','Charcoal Shower Gel, 250ml',70,20930),('2024-01-16','Coffee Face Care Kit',3,1874),('2024-01-16','Coffee Face Pack 50g',3,837),('2024-01-16','Coffee Face Pack, 50g',3,837),('2024-01-16','Coffee Face Scrub, 100g',28,8372),('2024-01-16','Coffee Face Scrub, 100g-',1,249),('2024-01-16','Coffee Face Wash, 100g',25,6225),('2024-01-16','Coffee Face Wash, 100g-',1,199),('2024-01-16','Coffee Face Wash, 50g',1,99),('2024-01-16','Coffee Face Wash, 50g (Pack of 2)',1,198),('2024-01-16','Coffee Face Wash, 50g-',1,79),('2024-01-16','Coffee Peel Off Mask, 60g',2,398),('2024-01-16','Coffee Revitalising Skin Care Combo',1,558),('2024-01-16','Coffee Shaving Foam, 264g',10,2950),('2024-01-16','Complete Coffee Shaving Kit',2,1578),('2024-01-16','Daily Intimate Wash-',1,149),('2024-01-16','Deep Clean Face & Body Wash',39,13455),('2024-01-16','Deep Cleansing Bath Soap',3,585),('2024-01-16','E-gift Card',3,3000),('2024-01-16','Face Towel',1,195),('2024-01-16','Feather Blades (Pack Of 20)',4,2000),('2024-01-16','Flexi Stud Razor (Pack of 5)',1,100),('2024-01-16','Free Gift (Use within 3 months)',772,0),('2024-01-16','Full Body Trimmer',8,31992),('2024-01-16','Gift Box(Holds 3 Products)',2,298),('2024-01-16','Globetrotter Perfume Kit for Men',1,795),('2024-01-16','Gotham, 100 ml',1,1995),('2024-01-16','Hair Styling Wax',1,395),('2024-01-16','Jodhpur Deodorant, 150ml (Pack of 2)',1,500),('2024-01-16','Landscaper 2.0 Groin Trimmer',10,19990),('2024-01-16','Mexico, 100 ml',39,31005),('2024-01-16','Moisturising Bath Soap (Pack of 3)',50,29250),('2024-01-16','Moisturising Face & Body Wash',21,7245),('2024-01-16','Moisturising Face & Body Wash-',2,498),('2024-01-16','Natural Beard Colour - Black',1,450),('2024-01-16','Neem & Charcoal Bath Soap (Pack of 3)',19,5643),('2024-01-16','Noir & Desire Combo',2,1420),('2024-01-16','OG Black Beard Trimmer',2,1798),('2024-01-16','Onion Beard Growth Oil, 30ml',40,15800),('2024-01-16','Oudh Body Spray, 150ml',65,25935),('2024-01-16','Oudh Body Spray, 150ml-',1,249),('2024-01-16','Post Shave Balm ,100g',9,3555),('2024-01-16','Post Shave Balm, 100g (Pack of 2)',1,790),('2024-01-16','Post-Shave Balm, 45g',2,398),('2024-01-16','Power Play Beard Trimmer',1,899),('2024-01-16','Power Styler Beard Trimmer',75,67425),('2024-01-16','Pre-Shave Scrub',12,3540),('2024-01-16','Precision Safety Razor - Silver Edition',3,4485),('2024-01-16','Premium Fragrances | Set of 4',2,1298),('2024-01-16','Premium MultiGroomer',12,24288),('2024-01-16','Razor Sharpener',2,198),('2024-01-16','Red Spice & Black Vibe Combo',1,299),('2024-01-16','Red Spice & Black Vibe Deodorant Combo, 150ml (Pack of 2)',5,3550),('2024-01-16','Red Spice Deo For Men, 150ml',38,13490),('2024-01-16','Red Spice Deo For Men, 150ml-',1,249),('2024-01-16','Refreshing Face and Body Wash',1,345),('2024-01-16','Sensi Flo4 Cartridge (Pack of 2)',9,2475),('2024-01-16','Sensi Flo4 Razor',2,598),('2024-01-16','Sensi Flo4 Razor & Cartridges (Pack of 4)',2,1198),('2024-01-16','Sensi Flo6 / Luxe Cartridge (Pack of 2)',11,6039),('2024-01-16','Sensi Flo6 / Luxe Cartridge (Pack of 4)',1,999),('2024-01-16','Sensi Flo6 Razor',9,3591),('2024-01-16','Sensi Flo6 Razor & Cartridges (Pack of 2)',2,1398),('2024-01-16','Sensi Flo6 Razor & Cartridges (Pack of 4)',1,999),('2024-01-16','Sensi Luxe Razor',2,1198),('2024-01-16','Sensi Smart3 Cartridge',3,850),('2024-01-16','Sensi Smart3 Cartridge (Pack of 2)',11,1639),('2024-01-16','Sensi Smart3 Cartridge (Pack of 4)',1,249),('2024-01-16','Sensi Smart3 Cartridges (Pack of 8)',7,3213),('2024-01-16','Sensi Smart3 Razor',7,693),('2024-01-16','Sensi Smart3 Razor & Cartridges (Pack of 2)',35,6965.35),('2024-01-16','Sensi Smart3 Razor & Cartridges (Pack of 4)',9,2691),('2024-01-16','Sensi Smart3 Razor-',2,198),('2024-01-16','Sensitive Shaving Foam (Pack of 2)',1,550),('2024-01-16','Sensitive Shaving Foam, 264g',25,6125),('2024-01-16','Sensitive Shaving Foam, 264g-',2,398),('2024-01-16','Sensitive Shaving Foam, 425g',5,1495),('2024-01-16','Shaving Cream | Tea Tree Oil & Aloe Vera, 100g',1,195),('2024-01-16','Shea Butter Bath Soap',5,625),('2024-01-16','Shea Butter Bath Soap-',4,396),('2024-01-16','Shea Butter Moisturizer, 100ml',28,8260),('2024-01-16','Spice Body Spray, 150ml',43,17157),('2024-01-16','Thank You Gift Box',1,99),('2024-01-16','Tokyo, 100 ml',22,17490),('2024-01-16','Travel Kit',5,745),('2024-01-16','Travel Kit-',6,594),('2024-01-16','Turmeric & Sandalwood After Shave Lotion, 100ml',63,18585),('2024-01-16','Turmeric & Sandalwood After Shave lotion 100ml-',1,249),('2024-01-16','Turmeric Face Wash, 100g',10,2490),('2024-01-16','Turmeric Shaving Cream, 78g',5,495),('2024-01-16','Turmeric Shaving Foam, 264g',19,5605),('2024-01-16','Two Good Two be True | Set of 2',1,1590),('2024-01-16','Veleno EDT, 100 ml',95,189525),('2024-01-16','Veleno Perfume, 30ml',22,17490),('2024-01-16','Venice, 30ml',371,554645),('2024-01-16','Vitamin C Face Serum, 30ML',62,36890),('2024-01-16','Wanderlust Perfume Kit For Men',1,1495),('2024-01-16','razor cartridges',1,285);
/*!40000 ALTER TABLE `bombayshavingtop_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bombayshavingtop_return_products`
--

DROP TABLE IF EXISTS `bombayshavingtop_return_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bombayshavingtop_return_products` (
  `date` date NOT NULL,
  `name` varchar(400) DEFAULT NULL,
  `return_quantity` int DEFAULT NULL,
  KEY `date_index` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bombayshavingtop_return_products`
--

LOCK TABLES `bombayshavingtop_return_products` WRITE;
/*!40000 ALTER TABLE `bombayshavingtop_return_products` DISABLE KEYS */;
INSERT INTO `bombayshavingtop_return_products` VALUES ('2024-01-16','Anti Acne Face Wash, 150g',1),('2024-01-16','Bearberry Body Yogurt',1),('2024-01-16','Beard Shaper Tool',1),('2024-01-16','Black Vibe Deo For Men, 150ml',1),('2024-01-16','Charcoal Bath Soap, 100g (Pack of 3)',2),('2024-01-16','Charcoal Face Sheet Mask (Pack of 2)',2),('2024-01-16','Charcoal Face Wash, 100g',3),('2024-01-16','Charcoal Hair Removal Spray, 200ml',4),('2024-01-16','Charcoal Shaving Foam, 425g',2),('2024-01-16','Charcoal Shower Gel, 250ml',1),('2024-01-16','Coffee Face Scrub, 100g',2),('2024-01-16','Coffee Face Wash, 100g',4),('2024-01-16','Deep Clean Face & Body Wash',2),('2024-01-16','Free Gift (Use within 3 months)',31),('2024-01-16','Full Body Trimmer',1),('2024-01-16','Landscaper 2.0 Groin Trimmer',1),('2024-01-16','Mexico, 100 ml',2),('2024-01-16','Moisturising Face & Body Wash-',1),('2024-01-16','Oudh Body Spray, 150ml',2),('2024-01-16','Post Shave Balm ,100g',1),('2024-01-16','Power Styler Beard Trimmer',7),('2024-01-16','Pre-Shave Scrub',1),('2024-01-16','Precision Safety Razor - Silver Edition',1),('2024-01-16','Red Spice Deo For Men, 150ml',2),('2024-01-16','Sensi Flo6 Razor & Cartridges (Pack of 2)',1),('2024-01-16','Sensi Smart3 Razor & Cartridges (Pack of 2)',1),('2024-01-16','Sensi Smart3 Razor & Cartridges (Pack of 4)',1),('2024-01-16','Shea Butter Moisturizer, 100ml',1),('2024-01-16','Spice Body Spray, 150ml',2),('2024-01-16','Tokyo, 100 ml',1),('2024-01-16','Travel Kit',1),('2024-01-16','Turmeric Face Wash, 100g',1),('2024-01-16','Turmeric Shaving Cream, 78g',1),('2024-01-16','Veleno Perfume, 30ml',1),('2024-01-16','Venice, 30ml',7),('2024-01-16','Wanderlust Perfume Kit For Men',1);
/*!40000 ALTER TABLE `bombayshavingtop_return_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'shops_insights'
--

--
-- Dumping routines for database 'shops_insights'
--
/*!50003 DROP PROCEDURE IF EXISTS `create_shop_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_shop_tables`( in in_shop_name varchar(100))
BEGIN
 DECLARE table_name1 VARCHAR(200);
    DECLARE table_name2 VARCHAR(200);
    DECLARE table_name3 VARCHAR(200);
    DECLARE table_name4 VARCHAR(200);

    IF in_shop_name IS NOT NULL THEN
        SET table_name1 = CONCAT(in_shop_name, 'insights');
        SET @query = CONCAT('CREATE TABLE ', table_name1, ' LIKE bombayshavinginsights');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET table_name2 = CONCAT(in_shop_name, 'top_products');
        SET @query = CONCAT('CREATE TABLE ', table_name2, ' LIKE bombayshavingtop_products');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET table_name3 = CONCAT(in_shop_name, 'top_channels');
        SET @query = CONCAT('CREATE TABLE ', table_name3, ' LIKE bombayshavingtop_channels');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        
        
        SET table_name4 = CONCAT(in_shop_name, 'top_return_products');
        SET @query = CONCAT('CREATE TABLE ', table_name4, ' LIKE bombayshavingtop_return_products');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
	
    END IF;

   

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `new_procedure` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_procedure`( in in_shop_name varchar(100))
BEGIN
 DECLARE table_name1 VARCHAR(200);
    DECLARE table_name2 VARCHAR(200);
    DECLARE table_name3 VARCHAR(200);
    DECLARE table_name4 VARCHAR(200);

    IF in_shop_name IS NOT NULL THEN
        SET table_name1 = CONCAT(in_shop_name, 'insights');
        SET @query = CONCAT('CREATE TABLE ', table_name1, ' LIKE bombayshavinginsights');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET table_name2 = CONCAT(in_shop_name, 'top_products');
        SET @query = CONCAT('CREATE TABLE ', table_name2, ' LIKE bombayshavingtop_products');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SET table_name3 = CONCAT(in_shop_name, 'top_channels');
        SET @query = CONCAT('CREATE TABLE ', table_name3, ' LIKE bombayshavingtop_channels');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        
        
        SET table_name4 = CONCAT(in_shop_name, 'top_return_products');
        SET @query = CONCAT('CREATE TABLE ', table_name4, ' LIKE bombayshavingintop_return_products');
        PREPARE stmt FROM @query;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
	
    END IF;

   

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-18 14:58:59
