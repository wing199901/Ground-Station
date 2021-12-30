-- phpMyAdmin SQL Dump
-- version 5.0.4deb2ubuntu5
-- https://www.phpmyadmin.net/
--
-- 主機： localhost:3306
-- 產生時間： 2021 年 12 月 30 日 17:20
-- 伺服器版本： 10.5.13-MariaDB-0ubuntu0.21.10.1
-- PHP 版本： 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `flightRecord`
--
CREATE DATABASE IF NOT EXISTS `flightRecord` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `flightRecord`;

-- --------------------------------------------------------

--
-- 資料表結構 `data`
--
-- 建立時間： 2021 年 12 月 30 日 09:14
--

DROP TABLE IF EXISTS `data`;
CREATE TABLE IF NOT EXISTS `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sessionId` int(11) NOT NULL,
  `deviceId` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `beacon` tinyint(1) NOT NULL,
  `landing` tinyint(1) NOT NULL,
  `strobes` tinyint(1) NOT NULL,
  `pitot` tinyint(1) NOT NULL,
  `ias` float NOT NULL,
  `verticalSpeed` float NOT NULL,
  `whiskeyCompass` double NOT NULL,
  `stall` tinyint(1) NOT NULL,
  `overspeed` tinyint(1) NOT NULL,
  `slipskid` int(11) NOT NULL,
  `turnrate` float NOT NULL,
  `roll` double NOT NULL,
  `heading` double NOT NULL,
  `pitch` double NOT NULL,
  `autopilot` tinyint(1) NOT NULL,
  `headingSel` double NOT NULL,
  `throttleLever` double NOT NULL,
  `propellerLever` int(11) NOT NULL,
  `magnetOs` int(11) NOT NULL,
  `rpm` float NOT NULL,
  `maxRpm` double NOT NULL,
  `fuelSelector` int(11) NOT NULL,
  `elevatorTrim` float NOT NULL,
  `parkingBrake` tinyint(1) NOT NULL,
  `landingGear` tinyint(1) NOT NULL,
  `flaps` int(11) NOT NULL,
  `pressure` float NOT NULL,
  `mach` float NOT NULL,
  `fuelWeight` double NOT NULL,
  `aoa` double NOT NULL,
  `sideSlip` double NOT NULL,
  `flightDirector` tinyint(1) NOT NULL,
  `flightDirectorPitch` int(11) NOT NULL,
  `flightDirectorBank` int(11) NOT NULL,
  `alternator` tinyint(1) NOT NULL,
  `battery` tinyint(1) NOT NULL,
  `avionics` tinyint(1) NOT NULL,
  `fuelPump` tinyint(1) NOT NULL,
  `altitude` int(11) NOT NULL,
  `elevatorAxis` int(11) NOT NULL,
  `aileronAxis` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `status` enum('normal','resetting','in_menu','pausing') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sessionId` (`sessionId`),
  KEY `deviceId` (`deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 資料表的關聯 `data`:
--   `sessionId`
--       `session` -> `id`
--   `deviceId`
--       `device` -> `id`
--

-- --------------------------------------------------------

--
-- 資料表結構 `device`
--
-- 建立時間： 2021 年 12 月 30 日 09:18
--

DROP TABLE IF EXISTS `device`;
CREATE TABLE IF NOT EXISTS `device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 資料表的關聯 `device`:
--

-- --------------------------------------------------------

--
-- 資料表結構 `session`
--
-- 建立時間： 2021 年 12 月 30 日 09:18
--

DROP TABLE IF EXISTS `session`;
CREATE TABLE IF NOT EXISTS `session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `StartTime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 資料表的關聯 `session`:
--

-- --------------------------------------------------------

--
-- 資料表結構 `session_device`
--
-- 建立時間： 2021 年 12 月 30 日 09:19
--

DROP TABLE IF EXISTS `session_device`;
CREATE TABLE IF NOT EXISTS `session_device` (
  `sessionid` int(11) NOT NULL,
  `deviceid` int(11) NOT NULL,
  KEY `deviceid` (`deviceid`),
  KEY `sessionid` (`sessionid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 資料表的關聯 `session_device`:
--   `deviceid`
--       `device` -> `id`
--   `sessionid`
--       `session` -> `id`
--

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `data`
--
ALTER TABLE `data`
  ADD CONSTRAINT `data_ibfk_1` FOREIGN KEY (`sessionId`) REFERENCES `session` (`id`),
  ADD CONSTRAINT `data_ibfk_2` FOREIGN KEY (`deviceId`) REFERENCES `device` (`id`);

--
-- 資料表的限制式 `session_device`
--
ALTER TABLE `session_device`
  ADD CONSTRAINT `session_device_ibfk_1` FOREIGN KEY (`deviceid`) REFERENCES `device` (`id`),
  ADD CONSTRAINT `session_device_ibfk_2` FOREIGN KEY (`sessionid`) REFERENCES `session` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
