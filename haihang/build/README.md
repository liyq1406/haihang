# 部署条件
+ 系统版本: Ubuntu 14.04
+ docker版本: 1.12.3


# 部署过程
Payment模块部署时需要依次启动四个容器 MySQL, Django, nginx以及swagger. 
+ MySQL: 数据库服务
+ Django: 核心服务
+ nginx: 代理gunicorn以及静态资源
+ swagger: API测试服务

**部署时请注意执行命令的路径**

## MySQL容器部署
请参考[mysql_hna](mysql_hna/README.md)

## Django容器部署
请参考[django_hna](django_hna/README.md)

## nginx容器部署
请参考[gunicorn-nginx](gunicorn_nginx/README.md)

## swagger容器部署
请参考[swagger](../swagger/README.md)

# 反馈
如果部署过程中遇到问题, 请[联系我们](bin.long@youruncloud.com), 不胜感激!
