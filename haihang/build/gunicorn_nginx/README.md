# 关于
本路径下文件用于构建Gunicorn代理nginx镜像, 服务于生产环境

# 用法
进入该目录执行如下命令
```bash
docker build -t gunicorn_nginx -f Dockerfile ../../
docker run -d -p 8001:80 -e BACKEND=192.168.3.222:8000 gunicorn_nginx
```
注意前置条件为gunicorn服务已经启动完毕.

# 测试
访问`0.0.0.0:8001/cms/login`即可. 
