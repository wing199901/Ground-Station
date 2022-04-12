-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- 主機： localhost
-- 產生時間： 2022 年 04 月 11 日 12:46
-- 伺服器版本： 10.3.29-MariaDB
-- PHP 版本： 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `flight_data`
--
CREATE DATABASE IF NOT EXISTS `flight_data` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `flight_data`;

-- --------------------------------------------------------

--
-- 資料表結構 `data`
--

CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `device_id` varchar(4) NOT NULL,
  `time` datetime NOT NULL,
  `navigation` tinyint(1) NOT NULL,
  `beacon` tinyint(1) NOT NULL,
  `landing` tinyint(1) NOT NULL,
  `taxi` tinyint(1) NOT NULL,
  `strobes` tinyint(1) NOT NULL,
  `pitot` tinyint(1) NOT NULL,
  `ias` double NOT NULL,
  `verticalSpeed` double NOT NULL,
  `whiskeyCompass` double NOT NULL,
  `stall` tinyint(1) NOT NULL,
  `overspeed` tinyint(1) NOT NULL,
  `slipSkid` double NOT NULL,
  `turnRate` double NOT NULL,
  `pitch` double NOT NULL,
  `roll` double NOT NULL,
  `heading` double NOT NULL,
  `autopilot` tinyint(1) NOT NULL,
  `headingSel` double NOT NULL,
  `altitudeSel` double NOT NULL,
  `airspeedSel` double NOT NULL,
  `throttleLever` double NOT NULL,
  `propellerLever` double NOT NULL,
  `mixtureLever` double NOT NULL,
  `magnetos` int(1) NOT NULL,
  `rpm` double NOT NULL,
  `maxRPM` double NOT NULL,
  `fuelSelector` int(1) NOT NULL,
  `elevatorTrim` double NOT NULL,
  `parkingBrake` tinyint(1) NOT NULL,
  `landingGear` tinyint(1) NOT NULL,
  `flaps` int(1) NOT NULL,
  `pressure` double NOT NULL,
  `mach` double NOT NULL,
  `fuelWeight` double NOT NULL,
  `aoa` double NOT NULL,
  `sideSlip` double NOT NULL,
  `flightDirector` tinyint(1) NOT NULL,
  `flightDirectorPitch` double NOT NULL,
  `flightDirectorBank` double NOT NULL,
  `alternator` tinyint(1) NOT NULL,
  `battery` tinyint(1) NOT NULL,
  `avionics` tinyint(1) NOT NULL,
  `fuelPump` tinyint(1) NOT NULL,
  `altitude` double NOT NULL,
  `elevatorAxis` double NOT NULL,
  `aileronAxis` double NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `status` enum('normal','resetting','in_menu','pausing','offline') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `device`
--

CREATE TABLE `device` (
  `id` varchar(4) NOT NULL,
  `name` varchar(17) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `session`
--

CREATE TABLE `session` (
  `id` int(11) NOT NULL,
  `startTime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 資料表結構 `session_device`
--

CREATE TABLE `session_device` (
  `session_id` int(11) NOT NULL,
  `device_id` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessionId` (`session_id`),
  ADD KEY `deviceId` (`device_id`);

--
-- 資料表索引 `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `session`
--
ALTER TABLE `session`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `data`
--
ALTER TABLE `data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `session`
--
ALTER TABLE `session`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `data`
--
ALTER TABLE `data`
  ADD CONSTRAINT `data_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `session` (`id`),
  ADD CONSTRAINT `data_ibfk_2` FOREIGN KEY (`device_id`) REFERENCES `device` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
