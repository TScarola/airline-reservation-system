-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 26, 2022 at 05:04 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `air_ticket_reservation_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
CREATE TABLE IF NOT EXISTS `airline` (
  `name` varchar(20) NOT NULL,
  `airport_code` char(3) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `airport_code` (`airport_code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`, `airport_code`) VALUES
('China Eastern', 'PVG');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

DROP TABLE IF EXISTS `airplane`;
CREATE TABLE IF NOT EXISTS `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `id` int(11) NOT NULL,
  `num_seats` int(11) DEFAULT NULL,
  `manufacturer` varchar(50) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`airline_name`),
  KEY `airline_name` (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `id`, `num_seats`, `manufacturer`, `age`) VALUES
('China Eastern', 737, 149, 'Boeing', 3),
('JetBlue', 123, 87, 'Airbus', 8),
('Spirit Airlines', 4, 33, 'Comac', 15);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `code` char(3) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`code`, `name`, `city`, `country`, `type`) VALUES
('JFK', 'John F Kennedy', 'New York City', 'United States', 'International'),
('PVG', 'Shanghai Pudong', 'Shanghai', 'China', 'International'),
('qwe', 'qwe', 'qweq', 'qweqwe', 'domestic');

-- --------------------------------------------------------

--
-- Table structure for table `attending`
--

DROP TABLE IF EXISTS `attending`;
CREATE TABLE IF NOT EXISTS `attending` (
  `staff_username` varchar(50) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `departure_date` datetime NOT NULL,
  `flight_number` int(11) NOT NULL,
  PRIMARY KEY (`staff_username`,`airline_name`,`departure_date`,`flight_number`),
  KEY `airline_name` (`airline_name`,`departure_date`,`flight_number`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `building_number` varchar(50) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `passport_country` varchar(50) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `password`, `name`, `building_number`, `street`, `city`, `state`, `phone_number`, `date_of_birth`, `passport_country`, `passport_expiration`, `passport_number`) VALUES
('JSmith@gmail.com', 'password', 'John Smith', '123', 'Park Place', 'Manhattan', 'NY', '5679546215', '1993-08-14', 'United States', '2024-07-26', '533380006'),
('Thomasscarola1@gmail.com', 'p@nts33', 'Thomas Scarola', '228', 'Jay Street', 'Brooklyn', 'NY', '9082225642', '2000-09-24', 'United States', '2028-09-29', 'C03005988'),
('AChen3@gmail.com', 'fgon56wnio6', 'Alex Chen', '64', 'Dian Xin Shi Ye Bu', 'Beijing', 'FangShan', '3073329896', '1997-11-30', 'China', '2025-04-03', '10000G106');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
CREATE TABLE IF NOT EXISTS `flight` (
  `departure_date` datetime NOT NULL,
  `number` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `departure_airport` varchar(50) DEFAULT NULL,
  `arrival_airport` varchar(50) DEFAULT NULL,
  `arrival_date` datetime DEFAULT NULL,
  `base_price` float DEFAULT NULL,
  `plane_id` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`departure_date`,`number`,`airline_name`),
  KEY `airline_name` (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`departure_date`, `number`, `airline_name`, `departure_airport`, `arrival_airport`, `arrival_date`, `base_price`, `plane_id`, `status`) VALUES
('2022-04-24 00:00:00', 9843, 'China Eastern', 'PVG', 'JFK', '2022-04-25 00:00:00', 127.56, '737', 'On Time'),
('2022-04-15 00:00:00', 3646, 'JetBlue', 'LAX', 'JFK', '2022-04-15 00:00:00', 87.35, '123', 'on-time');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `username` varchar(50) NOT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`),
  KEY `airline_name` (`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`username`, `airline_name`, `password`, `first_name`, `last_name`, `date_of_birth`, `phone_number`) VALUES
('RAkana123', 'China Eastern', 'kjnfg8udjn2398d98f4', 'Ron', 'Akana', '1958-09-15', '2563378425');

-- --------------------------------------------------------

--
-- Table structure for table `taking`
--

DROP TABLE IF EXISTS `taking`;
CREATE TABLE IF NOT EXISTS `taking` (
  `customer_email` varchar(50) NOT NULL,
  `departure_date` datetime NOT NULL,
  `flight_number` int(11) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  PRIMARY KEY (`customer_email`,`departure_date`,`flight_number`,`airline_name`),
  KEY `departure_date` (`departure_date`,`flight_number`,`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
CREATE TABLE IF NOT EXISTS `ticket` (
  `id` varchar(50) NOT NULL,
  `customer_email` varchar(50) DEFAULT NULL,
  `departure_date` datetime DEFAULT NULL,
  `flight_number` int(11) DEFAULT NULL,
  `airline_name` varchar(50) DEFAULT NULL,
  `class` varchar(50) DEFAULT NULL,
  `sold_price` float DEFAULT NULL,
  `card_type` varchar(50) DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL,
  `card_expiration` date DEFAULT NULL,
  `purchase_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_email` (`customer_email`),
  KEY `departure_date` (`departure_date`,`flight_number`,`airline_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`id`, `customer_email`, `departure_date`, `flight_number`, `airline_name`, `class`, `sold_price`, `card_type`, `card_number`, `card_expiration`, `purchase_date`) VALUES
('996482', 'JSmith@gmail.com', '2022-04-07 00:00:00', 9843, 'China Eastern', 'Business', 127.56, 'credit', '56843365842156', '2024-07-12', '2022-03-06 00:00:00'),
('123456', 'JSmith@gmail.com', '2022-05-15 00:00:00', 1234, 'China Eastern', 'Economy', 100.43, 'credit', '56843365842156', '2024-07-12', '2022-04-07 00:00:00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
