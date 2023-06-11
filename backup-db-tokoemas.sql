CREATE DATABASE  IF NOT EXISTS `db_toko` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_toko`;
-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: 128.199.195.208    Database: db_toko
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.10.2

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
-- Table structure for table `barang`
--

DROP TABLE IF EXISTS `barang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `barang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama_barang` varchar(255) NOT NULL,
  `gram` varchar(255) NOT NULL,
  `tgl_input` varchar(255) NOT NULL,
  `tgl_update` varchar(255) DEFAULT NULL,
  `filename` varchar(225) NOT NULL,
  `qrcode` varchar(255) NOT NULL,
  `rec_id` varchar(255) DEFAULT NULL,
  `kadar` varchar(255) NOT NULL,
  `kodeqr` varchar(255) DEFAULT NULL,
  `tgl_new` varchar(225) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kodeqr_UNIQUE` (`kodeqr`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `barang`
--

LOCK TABLES `barang` WRITE;
/*!40000 ALTER TABLE `barang` DISABLE KEYS */;
/*!40000 ALTER TABLE `barang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kategori`
--

DROP TABLE IF EXISTS `kategori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kategori` (
  `id_kategori` int NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(255) NOT NULL,
  `tgl_input` varchar(255) NOT NULL,
  PRIMARY KEY (`id_kategori`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kategori`
--

LOCK TABLES `kategori` WRITE;
/*!40000 ALTER TABLE `kategori` DISABLE KEYS */;
INSERT INTO `kategori` VALUES (1,'ATK','7 May 2017, 10:23'),(5,'Sabun','7 May 2017, 10:28'),(6,'Snack','6 October 2020, 0:19'),(7,'Minuman','6 October 2020, 0:20');
/*!40000 ALTER TABLE `kategori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `id_login` int NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `id_member` int NOT NULL,
  PRIMARY KEY (`id_login`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (1,'admin','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5',1);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id_member` int NOT NULL AUTO_INCREMENT,
  `nm_member` varchar(255) NOT NULL,
  `alamat_member` text NOT NULL,
  `telepon` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `gambar` text NOT NULL,
  `NIK` text NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `level` varchar(255) NOT NULL,
  PRIMARY KEY (`id_member`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'Moli','uj harapan','081234567890','example@gmail.com','unnamed.jpg','12314121','admin','5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5','admin');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nota`
--

DROP TABLE IF EXISTS `nota`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nota` (
  `id_nota` int NOT NULL AUTO_INCREMENT,
  `id_barang` varchar(255) NOT NULL,
  `id_member` int NOT NULL,
  `jumlah` varchar(255) NOT NULL,
  `total` varchar(255) NOT NULL,
  `tanggal_input` varchar(255) NOT NULL,
  `periode` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_nota`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nota`
--

LOCK TABLES `nota` WRITE;
/*!40000 ALTER TABLE `nota` DISABLE KEYS */;
INSERT INTO `nota` VALUES (1,'BR001',1,'4','12000','6 October 2020, 0:45','10-2020'),(2,'BR001',1,'4','12000','6 October 2020, 0:45','10-2020'),(3,'BR001',1,'4','12000','6 October 2020, 0:45','10-2020'),(4,'BR001',1,'4','12000','6 October 2020, 0:45','10-2020'),(5,'BR001',1,'2','6000','6 October 2020, 0:49','10-2020'),(6,'BR001',1,'2','6000','6 October 2020, 0:49','10-2020'),(7,'BR001',1,'2','6000','6 October 2020, 1:15','10-2020'),(8,'BR002',1,'2','6000','6 October 2020, 1:17','10-2020'),(9,'BR001',1,'2','6000','6 October 2020, 1:20','10-2020'),(10,'BR003',1,'1','2000','5 April 2023, 21:46','04-2023');
/*!40000 ALTER TABLE `nota` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penjualan`
--

DROP TABLE IF EXISTS `penjualan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `penjualan` (
  `id_penjualan` int NOT NULL AUTO_INCREMENT,
  `id_barang` varchar(255) DEFAULT NULL,
  `id_member` varchar(225) DEFAULT NULL,
  `filename` varchar(225) DEFAULT NULL,
  `nama_konsumen` varchar(255) DEFAULT NULL,
  `id_transaksi` varchar(225) DEFAULT NULL,
  `harga_jual` varchar(255) DEFAULT NULL,
  `jumlah` varchar(255) DEFAULT NULL,
  `potongan_harga` varchar(255) DEFAULT NULL,
  `total` varchar(255) DEFAULT NULL,
  `gram` varchar(255) DEFAULT NULL,
  `tanggal_transaksi` varchar(255) DEFAULT NULL,
  `qrcode` varchar(255) DEFAULT NULL,
  `qrcode_transaksi` varchar(255) DEFAULT NULL,
  `nama_barang` varchar(225) DEFAULT NULL,
  `sub_total` varchar(255) DEFAULT NULL,
  `kasir` varchar(225) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `qtybrg` varchar(255) DEFAULT NULL,
  `tgl_nota` varchar(255) DEFAULT NULL,
  `no_hp` varchar(255) DEFAULT NULL,
  `kodeqr` varchar(255) DEFAULT NULL,
  `kadar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_penjualan`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penjualan`
--

LOCK TABLES `penjualan` WRITE;
/*!40000 ALTER TABLE `penjualan` DISABLE KEYS */;
/*!40000 ALTER TABLE `penjualan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_cart`
--

DROP TABLE IF EXISTS `tb_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_cart` (
  `idcart` int NOT NULL AUTO_INCREMENT,
  `id_barang` varchar(225) DEFAULT NULL,
  `filename` varchar(225) DEFAULT NULL,
  `nama_barang` varchar(225) DEFAULT NULL,
  `gram` varchar(225) DEFAULT NULL,
  `harga_jual` varchar(225) DEFAULT NULL,
  `harga_jual2` varchar(225) DEFAULT NULL,
  `qty` varchar(225) DEFAULT NULL,
  `tanggal_input` varchar(225) DEFAULT NULL,
  `tanggal_update` varchar(225) DEFAULT NULL,
  `qrcode` varchar(225) DEFAULT NULL,
  `potongan_harga` varchar(225) DEFAULT NULL,
  `potongan_harga2` varchar(225) DEFAULT NULL,
  `total` varchar(225) DEFAULT NULL,
  `jumlah` varchar(225) DEFAULT NULL,
  `kadar` varchar(255) DEFAULT NULL,
  `kodeqr` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idcart`),
  UNIQUE KEY `id_barang_UNIQUE` (`id_barang`)
) ENGINE=InnoDB AUTO_INCREMENT=204 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_cart`
--

LOCK TABLES `tb_cart` WRITE;
/*!40000 ALTER TABLE `tb_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tmpfoo`
--

DROP TABLE IF EXISTS `tmpfoo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tmpfoo` (
  `mykey` int(6) unsigned zerofill NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`mykey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tmpfoo`
--

LOCK TABLES `tmpfoo` WRITE;
/*!40000 ALTER TABLE `tmpfoo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tmpfoo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `toko`
--

DROP TABLE IF EXISTS `toko`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `toko` (
  `id_toko` int NOT NULL AUTO_INCREMENT,
  `nama_toko` varchar(255) NOT NULL,
  `alamat_toko` text NOT NULL,
  `tlp` varchar(255) NOT NULL,
  `nama_pemilik` varchar(255) NOT NULL,
  PRIMARY KEY (`id_toko`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `toko`
--

LOCK TABLES `toko` WRITE;
/*!40000 ALTER TABLE `toko` DISABLE KEYS */;
INSERT INTO `toko` VALUES (1,'Toko Emas Mulia Berau','Berau','081234567890','Moli');
/*!40000 ALTER TABLE `toko` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-11 23:30:43
