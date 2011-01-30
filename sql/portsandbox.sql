/*
 Navicat Premium Data Transfer

 Source Server         : sandbox
 Source Server Type    : MySQL
 Source Server Version : 50089
 Source Host           : 172.16.48.128
 Source Database       : portsandbox

 Target Server Type    : MySQL
 Target Server Version : 50089
 File Encoding         : utf-8

 Date: 02/14/2011 21:04:09 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `BuildDepends`
-- ----------------------------
DROP TABLE IF EXISTS `BuildDepends`;
CREATE TABLE `BuildDepends` (
  `Id` int(11) NOT NULL,
  `PortName` text NOT NULL,
  `PortLog` text,
  `CheckSumControl` int(11) default NULL,
  `ExtractControl` int(11) default NULL,
  `PatchControl` int(11) default NULL,
  `BuildControl` int(11) default NULL,
  `InstallControl` int(11) default NULL,
  KEY `Id` (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `Jail`
-- ----------------------------
DROP TABLE IF EXISTS `Jail`;
CREATE TABLE `Jail` (
  `Id` int(11) NOT NULL auto_increment,
  `JailDir` text NOT NULL,
  `BuildDir` text NOT NULL,
  `JailName` text NOT NULL,
  `Releng` text NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `LibDepends`
-- ----------------------------
DROP TABLE IF EXISTS `LibDepends`;
CREATE TABLE `LibDepends` (
  `Id` int(11) NOT NULL,
  `PortName` text NOT NULL,
  `PortLog` text,
  `CheckSumControl` int(11) default NULL,
  `ExtractControl` int(11) default NULL,
  `PatchControl` int(11) default NULL,
  `BuildControl` int(11) default NULL,
  `InstallControl` int(11) default NULL,
  KEY `Id` (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `MainPort`
-- ----------------------------
DROP TABLE IF EXISTS `MainPort`;
CREATE TABLE `MainPort` (
  `Id` int(11) NOT NULL,
  `PortName` text NOT NULL,
  `PortLog` text,
  `CheckSumControl` int(11) default NULL,
  `ExtractControl` int(11) default NULL,
  `PatchControl` int(11) default NULL,
  `BuildControl` int(11) default NULL,
  `InstallControl` int(11) default NULL,
  `DeinstallControl` int(11) default NULL,
  `PackageControl` int(11) default NULL,
  `Committer` text,
  `MtreeControl` int(11) default NULL
) ENGINE=MyISAM AUTO_INCREMENT=326 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `NoBuild`
-- ----------------------------
DROP TABLE IF EXISTS `NoBuild`;
CREATE TABLE `NoBuild` (
  `id` int(11) default NULL,
  `PortName` text,
  `Category` text,
  `NoPackage` int(11) default NULL,
  `NoCdrom` int(11) default NULL,
  `Restricted` int(11) default NULL,
  `Forbidden` int(11) default NULL,
  `Broken` int(11) default NULL,
  `Deprecated` int(11) default NULL,
  `NoPackageMsg` text,
  `NoCdromMsg` text,
  `RestrictedMsg` text,
  `ForbiddenMsg` text,
  `BrokenMsg` text,
  `DeprecatedMsg` text,
  `IgnoreMsg` text,
  `Ignorec` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `Queue`
-- ----------------------------
DROP TABLE IF EXISTS `Queue`;
CREATE TABLE `Queue` (
  `Id` int(11) NOT NULL auto_increment,
  `Port` text,
  `StartBuild` text,
  `EndBuild` text,
  `Status` int(11) default NULL,
  `StatusBuild` int(11) default NULL,
  `JailId` int(11) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=491 DEFAULT CHARSET=latin1;

-- ----------------------------
--  Table structure for `RunDepends`
-- ----------------------------
DROP TABLE IF EXISTS `RunDepends`;
CREATE TABLE `RunDepends` (
  `Id` int(11) NOT NULL,
  `PortName` text NOT NULL,
  `PortLog` text,
  `CheckSumControl` int(11) default NULL,
  `ExtractControl` int(11) default NULL,
  `PatchControl` int(11) default NULL,
  `BuildControl` int(11) default NULL,
  `InstallControl` int(11) default NULL,
  KEY `Id` (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

