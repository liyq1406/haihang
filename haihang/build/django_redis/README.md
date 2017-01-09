# 关于
本路径下文件用于构建redis镜像

# 用法
进入该目录执行如下命令
```bash
docker build -t redis-hna .
docker run --restart always --name redis -d -p 6699:6379  redis-hna
```
