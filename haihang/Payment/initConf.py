# -*- coding:utf-8 -*-

# BALANCE, CREDIT为创建账户时默认值
# NO_BALANCE_LEFT 下 balance < 0 账户不可用
# NO_CREDIT_LEFT 下 信用额度扣减完账户不可用
MODULE_PAYMENT_ACCOUNT = {
    'BALANCE': 0,
    'CREDIT': 100000,
    'STRATEGY': 'NO_CREDIT_LEFT',
    'ORDER_BY': 'create_time',
}

# 优惠码长度
MODULE_COUPON = {

    'COUPON_CODE_LEN': 8,
}

# 默认账单标题以及详情
MODULE_PAYMENT = {
    'SUBJECT': 'HNA CloudOS平台充值',
    'BODY': '充值金额将会打入您在HNA CloudOS平台的用户账户内, 供您使用海航提供的云服务',
    'REFUND_REASON': '7天无理由退款',
}

# 默认分页排序: 第一页,每页10项,降序
MODULE_PAGANITION = {
    'LIMIT': '10',
    'OFFSET': '0',
    'DESC': '1',
}

# commit 的时候请不要修改下面的值. 制作镜像时会sed替换
# create database haihang character set utf8;
ENV_INIT = {
    'MYSQL_USER': 'MYSQL_USER',
    'MYSQL_PASSWORD': 'MYSQL_PASSWORD',
    'MYSQL_DATABASE_NAME': 'MYSQL_DATABASE_NAME',
    'MYSQL_HOST': 'MYSQL_HOST',
    'MYSQL_PORT': 'MYSQL_PORT',
    'PUBLIC_HOST': 'PUBLIC_HOST',
    'PUBLIC_PORT': 'PUBLIC_PORT',
    'RANCHER_URL': 'RANCHER_URL',
    'REDIS_HOST': 'REDIS_HOST',
    'REDIS_PORT': 'REDIS_PORT',
    'REDIS_DB': '0',
    'ALERT_URL': 'ALERT_URL',
    'API_KEY': 'API_KEY',
    'API_PASS': 'API_PASS',
    'USER_SYSTEM_URL': 'USER_SYSTEM_URL',
}


# ENV_INIT = {
#     'MYSQL_USER': 'root',
#     'MYSQL_PASSWORD': '123456',
#     'MYSQL_DATABASE_NAME': 'haihang',
#     # 'MYSQL_PASSWORD': 'lynngoing',
#     'MYSQL_HOST': '127.0.0.1',
#     # 'MYSQL_PORT': '3399',
#     'MYSQL_PORT': '3306',
#     'PUBLIC_HOST': '112.95.153.98',
#     'PUBLIC_PORT': '58000',
#     'RANCHER_URL': 'http://54.222.130.139:3000/v1-usage/account/',
#     'REDIS_HOST': '127.0.0.1',
#     'REDIS_PORT': '6379',
#     'ALERT_URL': 'http://223.202.32.56:8078/mc/v1/message/receive/',
#     'API_KEY': '0D02C551372B79DE6E68',
#     'API_PASS': 'G4kqtMgJXndw8K5gfMjdnPTbDYNiWRTuiGsJmTgn',
#     'REDIS_DB': 0
# }

#
# ENV_INIT = {
#     'MYSQL_USER': 'root',
#     # 'MYSQL_PASSWORD': '123456',
#     'MYSQL_PASSWORD': 'lynngoing',
#     # 'MYSQL_HOST': '120.24.62.88',
#     'MYSQL_DATABASE_NAME': 'haihang',
#     'MYSQL_HOST': '127.0.0.1',
#     # 'MYSQL_PORT': '3399',
#     'MYSQL_PORT': '3306',
#     'PUBLIC_HOST': '112.95.153.98',
#     'PUBLIC_PORT': '58000',
#     'RANCHER_URL': 'http://54.222.160.97:3000/v1-usage/account/',
#     'REDIS_HOST': '127.0.0.1',
#     'REDIS_PORT': '6379',
#     'ALERT_URL': 'http://223.202.32.56:8078/mc/v1/message/receive/',
#     'API_KEY': '0D02C551372B79DE6E68',
#     'API_PASS': 'G4kqtMgJXndw8K5gfMjdnPTbDYNiWRTuiGsJmTgn',
#     'REDIS_DB': 0,
#     'USER_SYSTEM_URL':'http://54.223.138.247:8081/v1/projects/user/authentication'
# }
