

DROP TABLE IF EXISTS `accountcreation`;

CREATE TABLE `accountcreation` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `email` varchar(90) DEFAULT NULL,
  `username` varchar(90) DEFAULT NULL,
  `password` varchar(90) DEFAULT NULL,
  `role` varchar(90) DEFAULT NULL,
  `walletaddress` varchar(90) DEFAULT NULL,
  `usertype` varchar(90) DEFAULT NULL,
  `amount` int(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

/*Data for the table `accountcreation` */

insert  into `accountcreation`(`id`,`name`,`email`,`username`,`password`,`role`,`walletaddress`,`usertype`,`amount`) values 
(1,'Raji','raji@gmail.com','raji','raji','Provider','353acad8fa7b7e282da8cc70d305223109f3be32905d71442de175be407d0780','Normal',1000),
(2,'mala','mala@gmail.com','mala','mala','Customer','447bd1884519944a86f4c9203f97c0fe7d3349559a005ab25c1c6af41a7a7b98','Elite',1201),
(3,'kiruba','kiruba@gmail.com','kiruba','kiruba','Customer','a52733d9e0d1ed6062b16005671779a4fd36990f8bcf8492a54abb6cca091543','Normal',1000),
(4,'manisha','manisha@gmail.com','manisha','manisha','Provider','d0c3e5cfb89c925626eb8e4bc8e81765920c7096a4c0148ba0a4f057928c76cd','Normal',1000),
(5,'sam','sam@gmail.com','sam','sam','Customer','e96e02d8e47f2a7c03be5117b3ed175c52aa30fb22028cf9c96f261563577605','Premium',390),
(6,'meera','meera@gmail.com','meera','meera','Provider','177b773d483d3fe541cd127ca95b62d7099e80651206c6ab7d6aa63eaa3bdc2c','Normal',1000),
(7,'mahi','mahi@gmail.com','mahi','mahi','Customer','78d7a82604de80d2b191e92a96d23a2803c0a0e910a32a6744e3ecd41e4da4cf','Premium',897),
(8,'maniskkkk','maniskkkk@gmail.com','maniskkkk','maniskkkk','Provider','fb446f0344a8bcf378d6103eac34e46cd90dbcb005546fbfcd3ce622f7d8d730','Normal',1000),
(9,'uma','uma@gmail.com','uma','uma','Provider','e811eb7830249bae4b61145ae6e5f0933d7f890570d6ead6e78f89f04fd6aeb5','Normal',1000),
(10,'meena','meena@gmail.com','meena','meena','Customer','f9b87cab13a1f660ca0bf58ea1b0cbc7c4527fcac21046717be58db31344687e','Elite',296),
(11,'renu','renu@gmail.com','renu','renu','Customer','4b393bf4343ef1153f2d1067f28acd7b4f87c62ba9cf02138d5665bc6da09c33','Premium',790),
(12,'mano','mano@gmail.com','mano','mano','Customer','3ebf7a087f79ad7fb361e356b99d3f4a7b6916d7cb8e950be6e2bcb971daa6c6','Elite',60);

/*Table structure for table `carditem` */

DROP TABLE IF EXISTS `carditem`;

CREATE TABLE `carditem` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `uid` varchar(100) DEFAULT NULL,
  `pid` varchar(100) DEFAULT NULL,
  `purchasestatus` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4;

/*Data for the table `carditem` */

insert  into `carditem`(`id`,`uid`,`pid`,`purchasestatus`) values 
(1,'3','1','0'),
(2,'3','1','0'),
(3,'3','1','0'),
(4,'3','1','0'),
(5,'3','1','0'),
(6,'3','1','0'),
(7,'3','1','0'),
(8,'3','1','0'),
(9,'3','1','0'),
(10,'3','1','0'),
(11,'3','1','0'),
(12,'2','1','1'),
(13,'2','1','1'),
(14,'2','1','1'),
(15,'5','2','1'),
(16,'7','3','1'),
(17,'7','3','0'),
(18,'2','2','1'),
(19,'2','2','1'),
(20,'2','1','1'),
(21,'2','2','1'),
(22,'2','1','1'),
(23,'2','2','0'),
(24,'10','1','1'),
(25,'12','4','1');

/*Table structure for table `couponaccess` */

DROP TABLE IF EXISTS `couponaccess`;

CREATE TABLE `couponaccess` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `uid` varchar(90) DEFAULT NULL,
  `counponAddress` varchar(90) DEFAULT NULL,
  `status` varchar(90) DEFAULT NULL,
  `giftAddress` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Data for the table `couponaccess` */

insert  into `couponaccess`(`id`,`uid`,`counponAddress`,`status`,`giftAddress`) values 
(1,'2','1','Purchase','3'),
(2,'3','1','Download',NULL),
(3,'2','1','Purchase',NULL),
(4,'2','1','Purchase',NULL),
(5,'5','2','Purchase',NULL),
(6,'5','1','Gift','2'),
(7,'2','6','Download',NULL),
(8,'2','2','Purchase','5'),
(9,'5','2','Download',NULL),
(10,'7','3','Purchase',NULL),
(11,'7','1','Gift','2'),
(12,'2','1','Purchase',NULL),
(13,'2','3','Purchase',NULL),
(14,'2','2','Purchase',NULL),
(15,'2','3','Purchase',NULL),
(16,'2','1','Purchase',NULL),
(17,'2','4','Purchase',NULL),
(18,'2','5','Purchase',NULL),
(19,'10','6','Purchase',NULL),
(20,'11','6','Download',NULL),
(21,'12','10','Purchase',NULL),
(22,'12','6','Download',NULL);

/*Table structure for table `ecoupon` */

DROP TABLE IF EXISTS `ecoupon`;

CREATE TABLE `ecoupon` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `uid` int(90) DEFAULT NULL,
  `date` varchar(90) DEFAULT NULL,
  `name` varchar(90) DEFAULT NULL,
  `couponcount` varchar(90) DEFAULT NULL,
  `price` varchar(90) DEFAULT NULL,
  `validitydate` varchar(90) DEFAULT NULL,
  `counponAddress` varchar(90) DEFAULT NULL,
  `contractCoupon` varchar(90) DEFAULT NULL,
  `percentage` varchar(90) DEFAULT NULL,
  `intialcouponcount` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `ecoupon` */

insert  into `ecoupon`(`id`,`uid`,`date`,`name`,`couponcount`,`price`,`validitydate`,`counponAddress`,`contractCoupon`,`percentage`,`intialcouponcount`) values 
(1,1,'2022-10-10','SummerCoupon','5','100','2022-10-20','53f2885b1b7344f3558ae61a1bff88b5a43ed70f915560d39a3addc323d23887','CouponContract/1665951568.8560035.wallet','3','100'),
(2,1,'2022-09-09','Travel Coupon','7','50','2022-10-20','2dbade466de54ab92fc45014c0c9e9393514b8ffcc6b5f7bba32322545ce56d9','CouponContract/1665960687.0303853.wallet','50','300'),
(3,6,'2022-10-02','Deevali Offer','7','100','2022-10-20','b977f8c20e9b25c3e38f9f878c0b4a2246705e6f263b0316f229eaae476e8394','CouponContract/1665982176.1583116.wallet','30','30'),
(4,6,'2022-10-17','Collectio Mela','9','20','2022-10-21','56bf0b17157e5749e71fee50f6e2d432ff99aa064f8c5a0c8a8e073ec1bfba18','CouponContract/1666182989.6356037.wallet','10','10'),
(6,9,'2022-11-01','Collectio Mela','7','10','2022-11-02','975160b61700ca669e7b938fc7c922926224535183f3829e7982a58751a80a81','CouponContract/1667453328.5466466.wallet','10','10'),
(7,9,'2022-11-05','Collectio Mela22','10','10','2022-11-09','3c960fb93628cfcbe0742df361167580a5214f0a8cc9e42c7ad80e9a0d36f7a5','CouponContract/1667453381.8531263.wallet','20','10'),
(8,8,'2022-11-05','Collectio Mela33','10','10','2022-11-11','dd31d85da18ea32052c21a15cfd74cfddf6fb8de6564c0b6c18464c11c1276fd','CouponContract/1667453582.905371.wallet','10','10'),
(9,6,'2022-11-12','mela','10','100','2022-11-15','84b3110f42572d331d3404e55035fa2b11559357917e38aeb33e2e1483945bf2','CouponContract/1667453684.3749726.wallet','30','10'),
(10,9,'2022-11-01','coupon offer','9','10','2022-11-06','477bb92f8ef9eef78b3074cd13240b8029b18866049c5b256d31520cf41a4ff5','CouponContract/1667455356.0711179.wallet','30','10');

/*Table structure for table `performance` */

DROP TABLE IF EXISTS `performance`;

CREATE TABLE `performance` (
  `id` int(99) NOT NULL AUTO_INCREMENT,
  `name` varchar(99) DEFAULT NULL,
  `result` varchar(99) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

/*Data for the table `performance` */

insert  into `performance`(`id`,`name`,`result`) values 
(1,'RSA','636'),
(2,'HMac','6'),
(3,'ContractVerificationHmac','5038'),
(4,'ContractVerificationRSA','11038'),
(5,'ContractVerificationHmac','832'),
(6,'ContractVerificationHmac','151');

/*Table structure for table `productinfo` */

DROP TABLE IF EXISTS `productinfo`;

CREATE TABLE `productinfo` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `uid` varchar(90) DEFAULT NULL,
  `pname` varchar(90) DEFAULT NULL,
  `price` varchar(90) DEFAULT NULL,
  `description` varchar(90) DEFAULT NULL,
  `imageurl` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `productinfo` */

insert  into `productinfo`(`id`,`uid`,`pname`,`price`,`description`,`imageurl`) values 
(1,'1','Watch','300','very nice to look','Watch_53.jpg'),
(2,'4','Shoe','500','very nice to look','Shoe_63.jpg'),
(3,'6','Body Spary','1000','very nice to look','Body Spary_46.jpg'),
(4,'9','mehaa','100','very nice to look','mehaa_80.jpg');

/*Table structure for table `wallet` */

DROP TABLE IF EXISTS `wallet`;

CREATE TABLE `wallet` (
  `id` int(90) NOT NULL AUTO_INCREMENT,
  `walletaddress` varchar(90) DEFAULT NULL,
  `wallettype` varchar(90) DEFAULT NULL,
  `keydetails` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

/*Data for the table `wallet` */

insert  into `wallet`(`id`,`walletaddress`,`wallettype`,`keydetails`) values 
(1,'353acad8fa7b7e282da8cc70d305223109f3be32905d71442de175be407d0780','Member','WalletContract/raji.wallet'),
(2,'53f2885b1b7344f3558ae61a1bff88b5a43ed70f915560d39a3addc323d23887','Coupon','WalletContract/1665951568.8560035.wallet'),
(3,'447bd1884519944a86f4c9203f97c0fe7d3349559a005ab25c1c6af41a7a7b98','Member','WalletContract/mala.wallet'),
(4,'a52733d9e0d1ed6062b16005671779a4fd36990f8bcf8492a54abb6cca091543','Member','WalletContract/kiruba.wallet'),
(5,'d0c3e5cfb89c925626eb8e4bc8e81765920c7096a4c0148ba0a4f057928c76cd','Member','WalletContract/manisha.wallet'),
(6,'e96e02d8e47f2a7c03be5117b3ed175c52aa30fb22028cf9c96f261563577605','Member','WalletContract/sam.wallet'),
(7,'2dbade466de54ab92fc45014c0c9e9393514b8ffcc6b5f7bba32322545ce56d9','Coupon','WalletContract/1665960687.0303853.wallet'),
(8,'177b773d483d3fe541cd127ca95b62d7099e80651206c6ab7d6aa63eaa3bdc2c','Member','WalletContract/meera.wallet'),
(9,'b977f8c20e9b25c3e38f9f878c0b4a2246705e6f263b0316f229eaae476e8394','Coupon','WalletContract/1665982176.1583116.wallet'),
(10,'78d7a82604de80d2b191e92a96d23a2803c0a0e910a32a6744e3ecd41e4da4cf','Member','WalletContract/mahi.wallet'),
(11,'56bf0b17157e5749e71fee50f6e2d432ff99aa064f8c5a0c8a8e073ec1bfba18','Coupon','WalletContract/1666182989.6356037.wallet'),
(12,'fb446f0344a8bcf378d6103eac34e46cd90dbcb005546fbfcd3ce622f7d8d730','Member','WalletContract/maniskkkk.wallet'),
(13,'4fad826bbe95b09df662196b4c456961ebcc365fc20127145f0158457a8898cf','Coupon','WalletContract/1667221088.1383736.wallet'),
(14,'e811eb7830249bae4b61145ae6e5f0933d7f890570d6ead6e78f89f04fd6aeb5','Member','WalletContract/uma.wallet'),
(15,'f9b87cab13a1f660ca0bf58ea1b0cbc7c4527fcac21046717be58db31344687e','Member','WalletContract/meena.wallet'),
(16,'975160b61700ca669e7b938fc7c922926224535183f3829e7982a58751a80a81','Coupon','WalletContract/1667453328.5466466.wallet'),
(17,'3c960fb93628cfcbe0742df361167580a5214f0a8cc9e42c7ad80e9a0d36f7a5','Coupon','WalletContract/1667453381.8531263.wallet'),
(18,'dd31d85da18ea32052c21a15cfd74cfddf6fb8de6564c0b6c18464c11c1276fd','Coupon','WalletContract/1667453582.905371.wallet'),
(19,'84b3110f42572d331d3404e55035fa2b11559357917e38aeb33e2e1483945bf2','Coupon','WalletContract/1667453684.3749726.wallet'),
(20,'4b393bf4343ef1153f2d1067f28acd7b4f87c62ba9cf02138d5665bc6da09c33','Member','WalletContract/renu.wallet'),
(21,'477bb92f8ef9eef78b3074cd13240b8029b18866049c5b256d31520cf41a4ff5','Coupon','WalletContract/1667455356.0711179.wallet'),
(22,'3ebf7a087f79ad7fb361e356b99d3f4a7b6916d7cb8e950be6e2bcb971daa6c6','Member','WalletContract/mano.wallet');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
