# 关于
本路径下文件用于构建payment模块镜像

# 用法

**请先将module_payment下alipay以及paypal路径中config的账号相关信息替换.**

进入本文件所在路径执行如下命令
```bash
docker build -t payment-hna -f Dockerfile ../../
# 需要填写mysql相关参数, 公网地址
docker run -d --restart always \
           -e MYSQL_USER=root \
           -e MYSQL_PASSWORD=123456 \
           -e MYSQL_HOST=127.0.0.1 \
           -e MYSQL_PORT=3306  \
           -e PUBLIC_HOST=112.95.153.98 \
           -e PUBLIC_PORT=58000 \
           -e RANCHER_URL=http://54.223.81.211:3000/v1-usage/account/ \
           -e REDIS_HOST=127.0.0.1 \
           -e REDIS_PORT=6699 \
           -e REDIS_DB=0 \
           -e ALERT_URL=http://223.202.32.56:8078/mc/v1/message/receive/ \
           -e API_KEY=0D02C551372B79DE6E68 \
           -e API_PASS=G4kqtMgJXndw8K5gfMjdnPTbDYNiWRTuiGsJmTgn \
           -p 8000:8000 payment-hna
```

# 注意事项
+ 容器启动需要一定时间
+ 默认用户名密码在run.sh中
+ 如果重新启动该容器, 建议先删除数据库中的默认用户
