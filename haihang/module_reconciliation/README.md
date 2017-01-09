# 概要
该模块为对账模块, 提供如下功能
+ 对账异常查询
+ 对账异常处理

# API接口
+ 接口说明 详见`支付-对账模块详细设计说明`
+ 接口调试 访问`0.0.0.0:8000`, 通过swagger进行调试

# 测试
```
python manage.py test module_reconciliation
```
该命令将会运行本模块的测试用例, 测试数据在项目中fixtures文件夹下

# TODO
+ 接口暂时未做认证
