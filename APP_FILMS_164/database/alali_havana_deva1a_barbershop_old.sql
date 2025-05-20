DROP DATABASE IF EXISTS alali_havana_deva1_barbershop;
CREATE DATABASE IF NOT EXISTS alali_havana_deva1_barbershop;
USE alali_havana_deva1_barbershop;

-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.41 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;



-- Listage de la structure de table barbershop. clients
DROP TABLE IF EXISTS `t_clients`;
CREATE TABLE IF NOT EXISTS `t_clients` (
  `id_clients` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_clients`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des donnees de la table barbershop.clients : ~20 rows (environ)
INSERT INTO `t_clients` (`id_clients`, `nom`, `prenom`, `telephone`) VALUES
	(1, 'Muller', 'Hans', '0761234567'),
	(2, 'Schneider', 'Peter', '0799876543'),
	(3, 'Keller', 'Lucas', '0769876543'),
	(4, 'Weber', 'Markus', '0791234567'),
	(5, 'Bucher', 'Reto', '0786543210'),
	(6, 'Wenger', 'Nicolas', '0771237890'),
	(7, 'Brunner', 'Jonas', '0764567890'),
	(8, 'Gerber', 'David', '0794561237'),
	(9, 'Meier', 'Pascal', '0783214569'),
	(10, 'Hofmann', 'Daniel', '0774561238'),
	(11, 'Steiner', 'Oliver', '0767891234'),
	(12, 'Frei', 'Sandro', '0796784321'),
	(13, 'Kunz', 'Fabian', '0789871236'),
	(14, 'Hofer', 'Julian', '0776543219'),
	(15, 'Suter', 'Rafael', '0765432187'),
	(16, 'Baumann', 'Simon', '0794321876'),
	(17, 'Schmid', 'Adrian', '0785432167'),
	(18, 'Zaugg', 'Patrick', '0778765432'),
	(19, 'Stalder', 'Michael', '0763219874'),
	(20, 'Gassmann', 'Roman', '0797654321');

-- Listage de la structure de table barbershop. employes
DROP TABLE IF EXISTS `t_employes`;
CREATE TABLE IF NOT EXISTS `t_employes` (
  `id_employes` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  `specialite` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_employes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table barbershop.employes : ~3 rows (environ)
INSERT INTO `t_employes` (`id_employes`, `nom`, `prenom`, `telephone`, `specialite`) VALUES
	(1, 'Al Ali', 'Alan', '0787036426', 'Barbier'),
	(2, 'Al ALi', 'Sipan', '0782443511', 'Coiffeur'),
	(3, 'Al Ali', 'Rewan', '0786752700', 'Barbier');

-- Listage de la structure de table barbershop. evaluer
DROP TABLE IF EXISTS `t_evaluer`;
CREATE TABLE IF NOT EXISTS `t_evaluer` (
  `id_evaluer` int NOT NULL AUTO_INCREMENT,
  `FK_clients` int DEFAULT NULL,
  `FK_services` int DEFAULT NULL,
  `note` int DEFAULT NULL,
  `commentaire` text,
  `date_avis` date DEFAULT NULL,
  PRIMARY KEY (`id_evaluer`),
  KEY `FK_clients` (`FK_clients`),
  KEY `FK_services` (`FK_services`),
  CONSTRAINT `t_evaluer_ibfk_1` FOREIGN KEY (`FK_clients`) REFERENCES `t_clients` (`id_clients`),
  CONSTRAINT `t_evaluer_ibfk_2` FOREIGN KEY (`FK_services`) REFERENCES `t_services` (`id_services`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table barbershop.evaluer : ~5 rows (environ)
INSERT INTO `t_evaluer` (`id_evaluer`, `FK_clients`, `FK_services`, `note`, `commentaire`, `date_avis`) VALUES
	(1, 1, 1, 5, 'Service excellent et ambiance agreable!', '2022-01-07'),
	(2, 2, 2, 4, 'Bon rasage mais un peu long.', '2023-02-07'),
	(3, 3, 3, 5, 'Tres satisfait de la coupe stylisee!', '2024-03-08'),
	(4, 4, 4, 4, 'Soin de la barbe tres bien fait.', '2025-01-08'),
	(5, 5, 5, 5, 'Coloration parfaite!', '2025-01-08');

-- Listage de la structure de table barbershop. executer
DROP TABLE IF EXISTS `t_executer`;
CREATE TABLE IF NOT EXISTS `t_executer` (
  `id_executer` int NOT NULL AUTO_INCREMENT,
  `FK_employes` int DEFAULT NULL,
  `FK_services` int DEFAULT NULL,
  `duree_effective` int DEFAULT NULL,
  PRIMARY KEY (`id_executer`),
  KEY `FK_employes` (`FK_employes`),
  KEY `FK_services` (`FK_services`),
  CONSTRAINT `t_executer_ibfk_1` FOREIGN KEY (`FK_employes`) REFERENCES `t_employes` (`id_employes`),
  CONSTRAINT `t_executer_ibfk_2` FOREIGN KEY (`FK_services`) REFERENCES `t_services` (`id_services`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table barbershop.executer : ~5 rows (environ)
INSERT INTO `t_executer` (`id_executer`, `FK_employes`, `FK_services`, `duree_effective`) VALUES
	(1, 1, 1, 35),
	(2, 2, 2, 45),
	(3, 3, 3, 40),
	(4, 1, 4, 30),
	(5, 2, 5, 60);

-- Listage de la structure de table barbershop. rencontrer
DROP TABLE IF EXISTS `t_rencontrer`;
CREATE TABLE IF NOT EXISTS `t_rencontrer` (
  `id_rencontrer` int NOT NULL AUTO_INCREMENT,
  `FK_clients` int DEFAULT NULL,
  `FK_employes` int DEFAULT NULL,
  `date_heure` datetime DEFAULT NULL,
  PRIMARY KEY (`id_rencontrer`),
  KEY `FK_clients` (`FK_clients`),
  KEY `FK_employes` (`FK_employes`),
  CONSTRAINT `t_rencontrer_ibfk_1` FOREIGN KEY (`FK_clients`) REFERENCES `t_clients` (`id_clients`),
  CONSTRAINT `t_rencontrer_ibfk_2` FOREIGN KEY (`FK_employes`) REFERENCES `t_employes` (`id_employes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table barbershop.rencontrer : ~10 rows (environ)
INSERT INTO `t_rencontrer` (`id_rencontrer`, `FK_clients`, `FK_employes`, `date_heure`) VALUES
	(1, 1, 1, '2025-03-07 10:30:00'),
	(2, 2, 2, '2025-03-07 11:00:00'),
	(3, 3, 1, '2025-03-08 09:30:00'),
	(4, 4, 2, '2025-03-08 10:00:00'),
	(5, 5, 1, '2025-03-08 10:30:00'),
	(6, 6, 2, '2025-03-08 11:00:00'),
	(7, 7, 3, '2025-03-08 11:30:00'),
	(8, 8, 1, '2025-03-08 12:00:00'),
	(9, 9, 2, '2025-03-08 12:30:00'),
	(10, 10, 3, '2025-03-08 13:00:00');

-- Listage de la structure de table barbershop. services
DROP TABLE IF EXISTS `t_services`;
CREATE TABLE IF NOT EXISTS `t_services` (
  `id_services` int NOT NULL AUTO_INCREMENT,
  `nom_service` varchar(255) DEFAULT NULL,
  `prix` decimal(10,2) DEFAULT NULL,
  `description` text,
  `duree` int DEFAULT NULL,
  PRIMARY KEY (`id_services`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table barbershop.services : ~5 rows (environ)
INSERT INTO `t_services` (`id_services`, `nom_service`, `prix`, `description`, `duree`) VALUES
	(1, 'Coupe classique', 35.00, 'Coupe de cheveux pour homme', 30),
	(2, 'Rasage a l ancienne', 40.00, 'Rasage traditionnel avec serviette chaude', 45),
	(3, 'Coupe stylisee', 50.00, 'Coupe de cheveux avec style moderne', 40),
	(4, 'Soin de la barbe', 30.00, 'Soin complet pour barbe', 30),
	(5, 'Coloration', 60.00, 'Coloration des cheveux', 60);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
