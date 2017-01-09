INSERT INTO `configure_configure`(`group_id`, `code`, `data_range`, `data_type`, `value`, `sort_order`, `create_time`, `remark`)
VALUES

(10, 'paypal_client_id',    '','string', '',               1 ,'2016-12-15 16:00:00', 'Paypal账号'),
(10, 'paypal_client_secret','','string', '',               2 ,'2016-12-15 16:00:00', 'Paypal密钥'),
(10, 'paypal_mode',         '','string', '',               3 ,'2016-12-15 16:00:00', 'Paypal运行模式'),

(11, 'alipay_partner',    '','string', '',                 1 ,'2016-12-15 16:00:00', '阿里商户账号'),
(11, 'alipay_key',        '','string', '',                 2 ,'2016-12-15 16:00:00', '阿里商户密钥'),
(11, 'alipay_seller_email','','string', '',                3 ,'2016-12-15 16:00:00', '阿里告警通知邮箱');



UPDATE `configure_configure` SET `value`='2088701254501517' WHERE code='alipay_partner';
UPDATE `configure_configure` SET `value`='vybjpzbnqhzv7vzfxvzczsnd2gkrdbg6' WHERE code='alipay_key';
UPDATE `configure_configure` SET `value`='alipay@cloudsoar.com' WHERE code='alipay_seller_email';


UPDATE `configure_configure` SET `value`='ATbyBZSSPIBySTZomTrAYtNmFrpYkJkM4NrVOm2HVH68rK5_kqBNEYK211K1Q9DX3hPA2-185FZfviy7' WHERE code='paypal_client_id';
UPDATE `configure_configure` SET `value`='EN-79i_VpgGO_hUqo3hUd4ilJrKkoE10tETbobosQ5em31NWRZTeBO5zJzOlnnK2qig9LCt9kEG3_b5k' WHERE code='paypal_client_secret';
UPDATE `configure_configure` SET `value`='sandbox' WHERE code='paypal_mode';


UPDATE `price_price` SET `price`=0.2 WHERE `host_model`='t2.micro';
UPDATE `price_price` SET `price`=0.4 WHERE `host_model`='t2.small';
UPDATE `price_price` SET `price`=0.8 WHERE `host_model`='t2.medium';
UPDATE `price_price` SET `price`=1.6 WHERE `host_model`='t2.large';