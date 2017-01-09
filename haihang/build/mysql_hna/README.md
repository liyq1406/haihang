# 关于
本路径下文件用于构建mysql镜像

# 用法
进入该目录执行如下命令
```bash
docker build -t mysql-hna .
docker run --restart always --name mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql-hna
```

# 备注
mysql启动后会执行init-payment.sql. 默认用户名:hna, 密码: hai11200
