# 关于
本项目为海航容器云平台支付模块项目

# 用法

## Docker方式运行
传送门: [Docker方式运行](build/README.md)

## 本地运行

准备条件:
+ python2.7.x
+ pip9.0.0
+ python-mysqldb
+ cron

如果你有一台ubuntu 14.04主机, 你可以按如下步骤搭建环境

```
apt-get update
apt-get install python pip python-mysqldb cron
pip install -r build/django_hna/requirements.txt
python manage.py migrate
python manage.py makemigrations
python manage.py runserver 0.0.0.0:8000

```

然后你将可以通过0.0.0.0:8000/apis/v1访问相关接口.

# 测试

如下命令将会运行各app的测试用例
```
python manage.py test
```

# 反馈
如果遇到问题, 请[联系我们](bin.long@youruncloud.com).
