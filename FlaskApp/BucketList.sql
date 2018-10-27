/*
Navicat MySQL Data Transfer

Source Server         : root
Source Server Version : 50723
Source Host           : localhost:3306
Source Database       : BucketList

Target Server Type    : MYSQL
Target Server Version : 50723
File Encoding         : 65001

Date: 2018-10-25 01:51:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ngo
-- ----------------------------
DROP TABLE IF EXISTS `ngo`;
CREATE TABLE `ngo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `lat` varchar(10) DEFAULT NULL,
  `lon` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of ngo
-- ----------------------------
INSERT INTO `ngo` VALUES ('1', 'dd', 'lol', 'ss', '23', '23');
INSERT INTO `ngo` VALUES ('2', 'Naru', 'naru@gmail.com', 'as', '46', '47');
INSERT INTO `ngo` VALUES ('3', 'sds', 'naru@gmail.com', 'as', '34', '45');
INSERT INTO `ngo` VALUES ('4', 'ds', 'naru@gmail.com', 'as', '36', '45');
INSERT INTO `ngo` VALUES ('5', 'ds', 'naru@gmail.com', 'as', '56', '57');
INSERT INTO `ngo` VALUES ('6', 'ds', 'naru@gmail.com', 'as', '22.22', '21.32');
INSERT INTO `ngo` VALUES ('7', 'sda', 'naru@gmail.com', 'as', '22.22', '21.32');
INSERT INTO `ngo` VALUES ('8', 'asd', 'naru@gmail.com', 'as', '22.22', '21.32');
INSERT INTO `ngo` VALUES ('9', 'dasd', 'naru@gmail.com', 'as', '22.22', '21.32');
INSERT INTO `ngo` VALUES ('10', 'dasd', 'naru@gmail.com', 'as', '22.22', '21.32');

-- ----------------------------
-- Table structure for ngo_saver
-- ----------------------------
DROP TABLE IF EXISTS `ngo_saver`;
CREATE TABLE `ngo_saver` (
  `id` int(11) NOT NULL,
  `rescue_lat` varchar(255) DEFAULT NULL,
  `rescue_lon` varchar(255) DEFAULT NULL,
  `rescue_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of ngo_saver
-- ----------------------------
INSERT INTO `ngo_saver` VALUES ('1', '32.0', '31.0', '3');
INSERT INTO `ngo_saver` VALUES ('1', '32.0', '31.0', '4');
INSERT INTO `ngo_saver` VALUES ('5', '54.0', '56.0', '1');
INSERT INTO `ngo_saver` VALUES ('5', '52.0', '53.0', '2');

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `pass` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of test
-- ----------------------------
INSERT INTO `test` VALUES ('1', 'dsd', 'sds', 'ds');
INSERT INTO `test` VALUES ('2', 'Naru', 'naru@gmail.com', 'djskjd');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lat` varchar(255) DEFAULT NULL,
  `lon` varchar(255) DEFAULT NULL,
  `rescue_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', '54', '56', '5');
INSERT INTO `user` VALUES ('2', '52', '53', '5');
INSERT INTO `user` VALUES ('3', '32', '31', '1');
INSERT INTO `user` VALUES ('4', '32', '31', '1');

-- ----------------------------
-- Procedure structure for sp_createUser
-- ----------------------------
DROP PROCEDURE IF EXISTS `sp_createUser`;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_name VARCHAR(20),
    IN p_email VARCHAR(20),
    IN p_pass VARCHAR(20)
)
BEGIN
    if ( select exists (select 1 from test where email = p_email) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into test
        (
            name,
            email,
            pass
        )
        values
        (
            p_name,
            p_email,
            p_pass
        );
     
    END IF;
END
;;
DELIMITER ;
SET FOREIGN_KEY_CHECKS=1;
