INSERT INTO `configure_configure`(`group_id`, `code`, `data_range`, `data_type`, `value`, `sort_order`, `create_time`, `remark`)
VALUES
(1, 'credit',               '',   'int', 10000,           1, '2016-12-15 16:00:00', '默认信用额度'),
(2, 'strategy',             '','string', 'NO_CREDIT_LEFT', 1 ,'2016-12-15 16:00:00', '账户冻结策略'),
(3, 'minor_alarm_days',     '','string', 15,               1 ,'2016-12-15 16:00:00', '第一次预警剩余天数'),
(4, 'critical_alarm_days',  '','string', 7,                1 ,'2016-12-15 16:00:00', '第二次预警剩余天数'),
(5, 'emergency_alarm_days', '','string', 3,                1 ,'2016-12-15 16:00:00', '第三次预警剩余天数'),
(6, 'sms_notify',           '','bool',   'True',           1 ,'2016-12-15 16:00:00', '短信通知'),
(7, 'email_notify',         '','bool',   'False',          1 ,'2016-12-15 16:00:00', '邮件通知'),
(8, 'min_remaining_days',   '','int',    1,                1 ,'2016-12-15 16:00:00', '账户余额下限，单位天'),
(9, 'redirect_url',         '','string', 'http://0.0.0.0:3001', 1 ,'2016-12-15 16:00:00', '付款回调地址');
