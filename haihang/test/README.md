# 关于
本文件夹主要描述API接口性能测试方法

# 准备工作
- 安装 ApacheBench, Version 2.3
- 一个运行着的Payment项目

# 测试方法
## GET类接口测试示例
在终端中运行`ab -n1000 -c100 http://cloudos.hnaresearch.com/ticket/list?user_id=21139`
测试结果如下:
```
Server Software:        nginx/1.10.2
Server Hostname:        cloudos.hnaresearch.com
Server Port:            80

Document Path:          /ticket/list?user_id=21139
Document Length:        601 bytes

Concurrency Level:      100
Time taken for tests:   4.818 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      976000 bytes
HTML transferred:       601000 bytes
Requests per second:    207.54 [#/sec] (mean)
Time per request:       481.825 [ms] (mean)
Time per request:       4.818 [ms] (mean, across all concurrent requests)
Transfer rate:          197.82 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       36   40   3.0     39      56
Processing:   156  423  66.2    423     648
Waiting:      156  423  66.2    423     647
Total:        194  463  67.0    462     704
```

## POST类接口测试示例
在终端中运行`ab -p post.txt -T application/json -n1000 -c100 http://54.222.160.114:8082/apis/v1/payments/`
测试结果如下:
```
Server Software:        nginx/1.4.6
Server Hostname:        54.222.160.114
Server Port:            8082

Document Path:          /apis/v1/payments/
Document Length:        853 bytes

Concurrency Level:      100
Time taken for tests:   9.158 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      1068000 bytes
Total body sent:        239000
HTML transferred:       853000 bytes
Requests per second:    109.20 [#/sec] (mean)
Time per request:       915.773 [ms] (mean)
Time per request:       9.158 [ms] (mean, across all concurrent requests)
Transfer rate:          113.89 [Kbytes/sec] received
                        25.49 kb/s sent
                        139.38 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       40   43   3.5     42      60
Processing:    60  828 136.3    862     936
Waiting:       60  828 136.3    862     936
Total:        102  870 135.1    903     995
```

# 备注
- 接口性能和服务器资源关系密切, 请确保硬件资源不是性能瓶颈
- 运行`ab -h`查看更多测试配置
- 其他接口请参考swagger文档进行测试