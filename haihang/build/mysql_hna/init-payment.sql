-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- 主机: 127.0.0.1
-- 生成日期: 2016 年 12 月 20 日 10:35
-- 服务器版本: 5.5.32
-- PHP 版本: 5.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `haihang`
--
CREATE DATABASE IF NOT EXISTS `haihang` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `haihang`;

-- --------------------------------------------------------

--
-- 表的结构 `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=85 ;

--
-- 转存表中的数据 `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can add permission', 2, 'add_permission'),
(5, 'Can change permission', 2, 'change_permission'),
(6, 'Can delete permission', 2, 'delete_permission'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add group', 4, 'add_group'),
(11, 'Can change group', 4, 'change_group'),
(12, 'Can delete group', 4, 'delete_group'),
(13, 'Can add content type', 5, 'add_contenttype'),
(14, 'Can change content type', 5, 'change_contenttype'),
(15, 'Can delete content type', 5, 'delete_contenttype'),
(16, 'Can add session', 6, 'add_session'),
(17, 'Can change session', 6, 'change_session'),
(18, 'Can delete session', 6, 'delete_session'),
(19, 'Can add payment account', 7, 'add_paymentaccount'),
(20, 'Can change payment account', 7, 'change_paymentaccount'),
(21, 'Can delete payment account', 7, 'delete_paymentaccount'),
(22, 'Can add account record', 8, 'add_accountrecord'),
(23, 'Can change account record', 8, 'change_accountrecord'),
(24, 'Can delete account record', 8, 'delete_accountrecord'),
(25, 'Can add coupon', 9, 'add_coupon'),
(26, 'Can change coupon', 9, 'change_coupon'),
(27, 'Can delete coupon', 9, 'delete_coupon'),
(28, 'Can add coupon user', 10, 'add_couponuser'),
(29, 'Can change coupon user', 10, 'change_couponuser'),
(30, 'Can delete coupon user', 10, 'delete_couponuser'),
(31, 'Can add coupon usage', 11, 'add_couponusage'),
(32, 'Can change coupon usage', 11, 'change_couponusage'),
(33, 'Can delete coupon usage', 11, 'delete_couponusage'),
(34, 'Can add payment', 12, 'add_payment'),
(35, 'Can change payment', 12, 'change_payment'),
(36, 'Can delete payment', 12, 'delete_payment'),
(37, 'Can add payment record', 13, 'add_paymentrecord'),
(38, 'Can change payment record', 13, 'change_paymentrecord'),
(39, 'Can delete payment record', 13, 'delete_paymentrecord'),
(40, 'Can add payment refund', 14, 'add_paymentrefund'),
(41, 'Can change payment refund', 14, 'change_paymentrefund'),
(42, 'Can delete payment refund', 14, 'delete_paymentrefund'),
(43, 'Can add reconciliation', 15, 'add_reconciliation'),
(44, 'Can change reconciliation', 15, 'change_reconciliation'),
(45, 'Can delete reconciliation', 15, 'delete_reconciliation'),
(46, 'Can add bill', 16, 'add_bill'),
(47, 'Can change bill', 16, 'change_bill'),
(48, 'Can delete bill', 16, 'delete_bill'),
(49, 'Can add bill record', 17, 'add_billrecord'),
(50, 'Can change bill record', 17, 'change_billrecord'),
(51, 'Can delete bill record', 17, 'delete_billrecord'),
(52, 'Can add month account record', 18, 'add_monthaccountrecord'),
(53, 'Can change month account record', 18, 'change_monthaccountrecord'),
(54, 'Can delete month account record', 18, 'delete_monthaccountrecord'),
(55, 'Can add price', 19, 'add_price'),
(56, 'Can change price', 19, 'change_price'),
(57, 'Can delete price', 19, 'delete_price'),
(58, 'Can add price add record', 20, 'add_priceaddrecord'),
(59, 'Can change price add record', 20, 'change_priceaddrecord'),
(60, 'Can delete price add record', 20, 'delete_priceaddrecord'),
(61, 'Can add alert level', 21, 'add_alertlevel'),
(62, 'Can change alert level', 21, 'change_alertlevel'),
(63, 'Can delete alert level', 21, 'delete_alertlevel'),
(64, 'Can add alert record', 22, 'add_alertrecord'),
(65, 'Can change alert record', 22, 'change_alertrecord'),
(66, 'Can delete alert record', 22, 'delete_alertrecord'),
(67, 'Can add user account', 23, 'add_useraccount'),
(68, 'Can change user account', 23, 'change_useraccount'),
(69, 'Can delete user account', 23, 'delete_useraccount'),
(70, 'Can add host statistic', 24, 'add_hoststatistic'),
(71, 'Can change host statistic', 24, 'change_hoststatistic'),
(72, 'Can delete host statistic', 24, 'delete_hoststatistic'),
(73, 'Can add host statistic plus', 25, 'add_hoststatisticplus'),
(74, 'Can change host statistic plus', 25, 'change_hoststatisticplus'),
(75, 'Can delete host statistic plus', 25, 'delete_hoststatisticplus'),
(76, 'Can add host statistic test', 26, 'add_hoststatistictest'),
(77, 'Can change host statistic test', 26, 'change_hoststatistictest'),
(78, 'Can delete host statistic test', 26, 'delete_hoststatistictest'),
(79, 'Can add host user', 27, 'add_hostuser'),
(80, 'Can change host user', 27, 'change_hostuser'),
(81, 'Can delete host user', 27, 'delete_hostuser'),
(82, 'Can add configure', 28, 'add_configure'),
(83, 'Can change configure', 28, 'change_configure'),
(84, 'Can delete configure', 28, 'delete_configure');

-- --------------------------------------------------------

--
-- 表的结构 `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `bill_bill`
--

CREATE TABLE IF NOT EXISTS `bill_bill` (
  `bill_uuid` char(32) NOT NULL,
  `bill_createtime` datetime NOT NULL,
  `host_uuid` char(32) NOT NULL,
  `name` varchar(50) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `run_time` double NOT NULL,
  `total_fee` double NOT NULL,
  `pay_status` tinyint(1) NOT NULL,
  `bill_status` tinyint(1) NOT NULL,
  `existed` tinyint(1) NOT NULL,
  `month` int(11) DEFAULT NULL,
  `bill_account_time` datetime DEFAULT NULL,
  PRIMARY KEY (`bill_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `bill_billrecord`
--

CREATE TABLE IF NOT EXISTS `bill_billrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_uuid` char(32) NOT NULL,
  `lifetime` double NOT NULL,
  `cpu` int(11) NOT NULL,
  `mem` int(11) NOT NULL,
  `disk` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `bill_monthaccountrecord`
--

CREATE TABLE IF NOT EXISTS `bill_monthaccountrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `month` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `pay_status` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `configure_configure`
--

CREATE TABLE IF NOT EXISTS `configure_configure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `code` varchar(128) NOT NULL,
  `data_range` varchar(128) NOT NULL,
  `data_type` varchar(32) NOT NULL,
  `value` longtext NOT NULL,
  `sort_order` int(11) NOT NULL,
  `remark` varchar(128) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

INSERT INTO `configure_configure`(`group_id`, `code`, `data_range`, `data_type`, `value`, `sort_order`, `create_time`, `remark`)
VALUES
(1, 'credit',               '','int',    0,                1, '2016-12-15 16:00:00', '默认信用额度,单位分'),
(2, 'strategy',             '','string', 'NO_CREDIT_LEFT', 1 ,'2016-12-15 16:00:00', '账户冻结策略'),
(3, 'minor_alarm_days',     '','int',    15,               1 ,'2016-12-15 16:00:00', '第一次预警剩余天数'),
(4, 'critical_alarm_days',  '','int',    7,                1 ,'2016-12-15 16:00:00', '第二次预警剩余天数'),
(5, 'emergency_alarm_days', '','int',    3,                1 ,'2016-12-15 16:00:00', '第三次预警剩余天数'),
(6, 'sms_notify',           '','bool',   'True',           1 ,'2016-12-15 16:00:00', '短信通知'),
(7, 'email_notify',         '','bool',   'False',          1 ,'2016-12-15 16:00:00', '邮件通知'),
(8, 'min_remaining_days',   '','int',    1,                1 ,'2016-12-15 16:00:00', '账户余额下限，单位天'),
(9, 'redirect_url',         '','string', 'http://0.0.0.0:3001', 1 ,'2016-12-15 16:00:00', '付款回调地址'),

(10, 'paypal_client_id',    '','string', '',               1 ,'2016-12-15 16:00:00', 'Paypal账号'),
(10, 'paypal_client_secret','','string', '',               2 ,'2016-12-15 16:00:00', 'Paypal密钥'),
(10, 'paypal_mode',         '','string', '',               3 ,'2016-12-15 16:00:00', 'Paypal运行模式'),

(11, 'alipay_partner',    '','string', '',                 1 ,'2016-12-15 16:00:00', '阿里商户账号'),
(11, 'alipay_key',        '','string', '',                 2 ,'2016-12-15 16:00:00', '阿里商户密钥'),
(11, 'alipay_seller_email','','string', '',                3 ,'2016-12-15 16:00:00', '阿里告警通知邮箱');



-- --------------------------------------------------------

--
-- 表的结构 `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
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
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=29 ;

--
-- 转存表中的数据 `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(4, 'auth', 'group'),
(2, 'auth', 'permission'),
(3, 'auth', 'user'),
(16, 'bill', 'bill'),
(17, 'bill', 'billrecord'),
(18, 'bill', 'monthaccountrecord'),
(28, 'configure', 'configure'),
(5, 'contenttypes', 'contenttype'),
(9, 'module_coupon', 'coupon'),
(11, 'module_coupon', 'couponusage'),
(10, 'module_coupon', 'couponuser'),
(12, 'module_payment', 'payment'),
(13, 'module_payment', 'paymentrecord'),
(14, 'module_payment', 'paymentrefund'),
(8, 'module_payment_account', 'accountrecord'),
(7, 'module_payment_account', 'paymentaccount'),
(15, 'module_reconciliation', 'reconciliation'),
(21, 'monitor', 'alertlevel'),
(22, 'monitor', 'alertrecord'),
(23, 'monitor', 'useraccount'),
(19, 'price', 'price'),
(20, 'price', 'priceaddrecord'),
(6, 'sessions', 'session'),
(24, 'statistic', 'hoststatistic'),
(25, 'statistic', 'hoststatisticplus'),
(26, 'statistic', 'hoststatistictest'),
(27, 'statistic', 'hostuser');

-- --------------------------------------------------------

--
-- 表的结构 `django_migrations`
--

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

--
-- 转存表中的数据 `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2016-12-29 01:28:25'),
(2, 'auth', '0001_initial', '2016-12-29 01:28:25'),
(3, 'admin', '0001_initial', '2016-12-29 01:28:25'),
(4, 'admin', '0002_logentry_remove_auto_add', '2016-12-29 01:28:26'),
(5, 'contenttypes', '0002_remove_content_type_name', '2016-12-29 01:28:26'),
(6, 'auth', '0002_alter_permission_name_max_length', '2016-12-29 01:28:26'),
(7, 'auth', '0003_alter_user_email_max_length', '2016-12-29 01:28:26'),
(8, 'auth', '0004_alter_user_username_opts', '2016-12-29 01:28:26'),
(9, 'auth', '0005_alter_user_last_login_null', '2016-12-29 01:28:26'),
(10, 'auth', '0006_require_contenttypes_0002', '2016-12-29 01:28:26'),
(11, 'auth', '0007_alter_validators_add_error_messages', '2016-12-29 01:28:26'),
(12, 'auth', '0008_alter_user_username_max_length', '2016-12-29 01:28:26'),
(13, 'sessions', '0001_initial', '2016-12-29 01:28:26'),
(14, 'bill', '0001_initial', '2016-12-29 01:28:38'),
(15, 'configure', '0001_initial', '2016-12-29 01:28:38'),
(16, 'module_coupon', '0001_initial', '2016-12-29 01:28:38'),
(17, 'module_payment', '0001_initial', '2016-12-29 01:28:38'),
(18, 'module_payment_account', '0001_initial', '2016-12-29 01:28:38'),
(19, 'module_reconciliation', '0001_initial', '2016-12-29 01:28:38'),
(20, 'monitor', '0001_initial', '2016-12-29 01:28:38'),
(21, 'price', '0001_initial', '2016-12-29 01:28:38'),
(22, 'statistic', '0001_initial', '2016-12-29 01:28:38');

-- --------------------------------------------------------

--
-- 表的结构 `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_coupon_coupon`
--

CREATE TABLE IF NOT EXISTS `module_coupon_coupon` (
  `coupon_uuid` char(32) NOT NULL,
  `coupon_code` varchar(8) NOT NULL,
  `coupon_type` varchar(20) NOT NULL,
  `coupon_value` int(11) NOT NULL,
  `coupon_using_count` int(11) NOT NULL,
  `coupon_using_user` int(11) NOT NULL,
  `using_user_left` int(11) NOT NULL,
  `valid_datetime_start` datetime NOT NULL,
  `valid_datetime_end` datetime NOT NULL,
  `limit_lower` int(11) NOT NULL,
  `limit_upper` int(11) NOT NULL,
  `theme` varchar(100) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`coupon_uuid`),
  UNIQUE KEY `coupon_code` (`coupon_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_coupon_couponusage`
--

CREATE TABLE IF NOT EXISTS `module_coupon_couponusage` (
  `coupon_usage_uuid` char(32) NOT NULL,
  `coupon_code` varchar(8) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `payment_account_uuid` char(32) NOT NULL,
  `use_time` datetime NOT NULL,
  `usage_source_type` varchar(20) NOT NULL,
  `usage_source_uuid` char(32) NOT NULL,
  `coupon_uuid_id` char(32) NOT NULL,
  PRIMARY KEY (`coupon_usage_uuid`),
  KEY `modu_coupon_uuid_id_c59a36e1_fk_module_coupon_coupon_coupon_uuid` (`coupon_uuid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_coupon_couponuser`
--

CREATE TABLE IF NOT EXISTS `module_coupon_couponuser` (
  `coupon_user_relate_uuid` char(32) NOT NULL,
  `coupon_code` varchar(8) NOT NULL,
  `coupon_type` varchar(20) NOT NULL,
  `coupon_value` int(11) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `payment_account_uuid` char(32) NOT NULL,
  `using_count_left` int(11) NOT NULL,
  `valid_datetime_start` datetime NOT NULL,
  `valid_datetime_end` datetime NOT NULL,
  `relate_time` datetime NOT NULL,
  `coupon_uuid_id` char(32) NOT NULL,
  PRIMARY KEY (`coupon_user_relate_uuid`),
  KEY `modu_coupon_uuid_id_e27698e2_fk_module_coupon_coupon_coupon_uuid` (`coupon_uuid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_payment_account_accountrecord`
--

CREATE TABLE IF NOT EXISTS `module_payment_account_accountrecord` (
  `account_record_uuid` char(32) NOT NULL,
  `modify_balance` double NOT NULL,
  `modify_source_type` varchar(50) NOT NULL,
  `modify_source_uuid` varchar(36) NOT NULL,
  `create_time` datetime NOT NULL,
  `payment_account_uuid_id` char(32) NOT NULL,
  PRIMARY KEY (`account_record_uuid`),
  KEY `D258a4fe1414accae9df16e217f00b50` (`payment_account_uuid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_payment_account_paymentaccount`
--

CREATE TABLE IF NOT EXISTS `module_payment_account_paymentaccount` (
  `payment_account_uuid` char(32) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `credit` double NOT NULL,
  `balance` double NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`payment_account_uuid`),
  UNIQUE KEY `user_uuid` (`user_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_payment_payment`
--

CREATE TABLE IF NOT EXISTS `module_payment_payment` (
  `payment_uuid` char(32) NOT NULL,
  `user_uuid` varchar(36) NOT NULL,
  `payment_account_uuid` varchar(36) NOT NULL,
  `payment_no` varchar(50) NOT NULL,
  `payment_price` int(11) NOT NULL,
  `paid_method` varchar(10) NOT NULL,
  `real_price` double NOT NULL,
  `sale_id` varchar(64) NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `coupon_uuid` varchar(36) NOT NULL,
  `coupon_code` varchar(10) NOT NULL,
  `paid_status` varchar(10) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`payment_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_payment_paymentrecord`
--

CREATE TABLE IF NOT EXISTS `module_payment_paymentrecord` (
  `payment_record_uuid` char(32) NOT NULL,
  `paid_method` varchar(10) NOT NULL,
  `pay_response_data` longtext NOT NULL,
  `create_time` datetime NOT NULL,
  `payment_uuid_id` char(32) NOT NULL,
  PRIMARY KEY (`payment_record_uuid`),
  KEY `payment_uuid_id_113dd057_fk_module_payment_payment_payment_uuid` (`payment_uuid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_payment_paymentrefund`
--

CREATE TABLE IF NOT EXISTS `module_payment_paymentrefund` (
  `payment_refund_uuid` char(32) NOT NULL,
  `refund_reason` varchar(300) NOT NULL,
  `refund_status` varchar(10) NOT NULL,
  `create_time` datetime NOT NULL,
  `payment_uuid_id` char(32) NOT NULL,
  PRIMARY KEY (`payment_refund_uuid`),
  KEY `payment_uuid_id_22e8f3ac_fk_module_payment_payment_payment_uuid` (`payment_uuid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `module_reconciliation_reconciliation`
--

CREATE TABLE IF NOT EXISTS `module_reconciliation_reconciliation` (
  `reconciliation_uuid` char(32) NOT NULL,
  `payment_no` varchar(50) DEFAULT NULL,
  `error_type` varchar(60) NOT NULL,
  `payment_record` longtext NOT NULL,
  `third_record` longtext NOT NULL,
  `deal_result` longtext NOT NULL,
  `deal_status` varchar(10) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`reconciliation_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `monitor_alertlevel`
--

CREATE TABLE IF NOT EXISTS `monitor_alertlevel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `low` int(11) NOT NULL,
  `medium` int(11) NOT NULL,
  `high` int(11) NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `monitor_alertrecord`
--

CREATE TABLE IF NOT EXISTS `monitor_alertrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) NOT NULL,
  `alert_number` int(11) NOT NULL,
  `alert_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `monitor_useraccount`
--

CREATE TABLE IF NOT EXISTS `monitor_useraccount` (
  `useraccount_uuid` char(32) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `payment_account_uuid` char(32) NOT NULL,
  PRIMARY KEY (`useraccount_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `price_price`
--

CREATE TABLE IF NOT EXISTS `price_price` (
  `created` datetime NOT NULL,
  `price_uuid` char(32) NOT NULL,
  `cpu` int(11) NOT NULL,
  `mem` int(11) NOT NULL,
  `disk` int(11) NOT NULL,
  `net` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `host_model` varchar(20) NOT NULL,
  `is_existed` tinyint(1) NOT NULL,
  `effective_date` date NOT NULL,
  PRIMARY KEY (`price_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `price_price`
--

INSERT INTO `price_price` (`created`, `price_uuid`, `cpu`, `mem`, `disk`, `net`, `price`, `host_model`, `is_existed`, `effective_date`) VALUES
('2016-12-21 03:08:29', 'bf3934cfc72a11e6936408002746aeaf', 1, 1024, 16, 'FREE', 0.2, 't2.micro', 1, '2016-12-20 08:00:00'),
('2016-12-21 03:24:09', 'ef8aac6ec72c11e6990a08002746aeaf', 1, 2048, 40, 'FREE', 0.4, 't2.small', 1, '2016-12-20 08:00:00'),
('2016-12-21 03:26:53', '514e71cfc72d11e6b20408002746aeaf', 2, 4096, 40, 'FREE', 0.8, 't2.medium', 1, '2016-12-20 08:00:00'),
('2016-12-21 03:30:09', 'c6174b8fc72d11e6941e08002746aeaf', 2, 8192, 40, 'FREE', 1.6, 't2.large', 1, '2016-12-20 08:00:00');

-- --------------------------------------------------------

--
-- 表的结构 `price_priceaddrecord`
--

CREATE TABLE IF NOT EXISTS `price_priceaddrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `price_uuid` char(32) NOT NULL,
  `create_time` datetime NOT NULL,
  `action` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `statistic_hoststatistic`
--

CREATE TABLE IF NOT EXISTS `statistic_hoststatistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `host_uuid` varchar(50) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `host_status` int(11) NOT NULL,
  `host_starttime` datetime NOT NULL,
  `host_cpu` int(11) NOT NULL,
  `host_mem` int(11) NOT NULL,
  `host_disk` int(11) NOT NULL,
  `host_net` varchar(50) NOT NULL,
  `run_time` int(11) NOT NULL,
  `record_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `statistic_hoststatisticplus`
--

CREATE TABLE IF NOT EXISTS `statistic_hoststatisticplus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `host_uuid` char(32) NOT NULL,
  `user_uuid` varchar(50) NOT NULL,
  `host_status` int(11) NOT NULL,
  `host_starttime` datetime NOT NULL,
  `host_cpu` int(11) NOT NULL,
  `host_mem` int(11) NOT NULL,
  `host_disk` int(11) NOT NULL,
  `host_net` varchar(50) NOT NULL,
  `host_time` int(11) NOT NULL,
  `record_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `statistic_hoststatistictest`
--

CREATE TABLE IF NOT EXISTS `statistic_hoststatistictest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `host_uuid` char(32) NOT NULL,
  `account_id` varchar(50) NOT NULL,
  `cpu` int(11) NOT NULL,
  `mem` int(11) NOT NULL,
  `disk` int(11) NOT NULL,
  `net` varchar(50) NOT NULL,
  `lifetime` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- 表的结构 `statistic_hostuser`
--

CREATE TABLE IF NOT EXISTS `statistic_hostuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `host_uuid` char(32) NOT NULL,
  `user_uuid` char(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 限制导出的表
--

--
-- 限制表 `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- 限制表 `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- 限制表 `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- 限制表 `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- 限制表 `module_coupon_couponusage`
--
ALTER TABLE `module_coupon_couponusage`
  ADD CONSTRAINT `modu_coupon_uuid_id_c59a36e1_fk_module_coupon_coupon_coupon_uuid` FOREIGN KEY (`coupon_uuid_id`) REFERENCES `module_coupon_coupon` (`coupon_uuid`);

--
-- 限制表 `module_coupon_couponuser`
--
ALTER TABLE `module_coupon_couponuser`
  ADD CONSTRAINT `modu_coupon_uuid_id_e27698e2_fk_module_coupon_coupon_coupon_uuid` FOREIGN KEY (`coupon_uuid_id`) REFERENCES `module_coupon_coupon` (`coupon_uuid`);

--
-- 限制表 `module_payment_account_accountrecord`
--
ALTER TABLE `module_payment_account_accountrecord`
  ADD CONSTRAINT `D258a4fe1414accae9df16e217f00b50` FOREIGN KEY (`payment_account_uuid_id`) REFERENCES `module_payment_account_paymentaccount` (`payment_account_uuid`);

--
-- 限制表 `module_payment_paymentrecord`
--
ALTER TABLE `module_payment_paymentrecord`
  ADD CONSTRAINT `payment_uuid_id_113dd057_fk_module_payment_payment_payment_uuid` FOREIGN KEY (`payment_uuid_id`) REFERENCES `module_payment_payment` (`payment_uuid`);

--
-- 限制表 `module_payment_paymentrefund`
--
ALTER TABLE `module_payment_paymentrefund`
  ADD CONSTRAINT `payment_uuid_id_22e8f3ac_fk_module_payment_payment_payment_uuid` FOREIGN KEY (`payment_uuid_id`) REFERENCES `module_payment_payment` (`payment_uuid`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
