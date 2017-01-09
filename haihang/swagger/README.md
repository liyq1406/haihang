# 关于
本路径下文件用于构建swagger-ui镜像, 以测试API

# 用法
进入该目录执行如下命令
```bash
docker build -t swagger-ui-hna .
# BACKEND为Django服务的地址, SWAGGER_UI为swagger_ui将要运行的地址, 请不要输入0.0.0.0等IP以免出现502
docker run -d -e BACKEND=192.168.3.222:8000 -e SWAGGER_UI=192.168.3.222:8085 -p 8085:80 swagger-ui-hna
```
你也可以使用docker-compose的方式
```bash
docker-compose -f docker-compose.yml up
```
# 测试API
访问`192.168.3.222:8085`即可. Enjoy!
