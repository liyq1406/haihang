# 关于
本路径下文件用于监控定时任务

# 用法
```
# 安装配置supervisor
sudo apt-get install supervisor
sudo cp *.conf /etc/supervisor/conf.d/
sudo supervisorctl reread 
sudo supervisorctl update

# 启动服务
sudo supervisorctl start payment_celery_worker
sudo supervisorctl start payment_celery_beat

# 停止服务
sudo supervisorctl stop payment_celery_worker
sudo supervisorctl stop payment_celery_beat

# 重启服务
sudo supervisorctl restart payment_celery_worker
sudo supervisorctl restart payment_celery_beat

# 查看服务状态
sudo supervisorctl status payment_celery_worker
sudo supervisorctl status payment_celery_beat
```

# 说明
- conf文件中的相关路径需要修改为自己本地路径
- payment_beat.log以及payment_worker.log为监控产生的日志文件