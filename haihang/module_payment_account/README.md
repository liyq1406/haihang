# 概要
该模块为用户账户模块, 提供如下功能
+ 创建用户账户
+ 修改用户账户
+ 账户余额变更
+ 账户信息查询(支持使用payment_account_uuid和user_uuid)
+ 变更记录查询(支持使用payment_account_uuid和user_uuid)

# API接口
+ 接口说明 详见`用户账户模块详细设计说明`
+ 接口调试 访问`0.0.0.0:8000`, 通过swagger进行调试

# 测试
```
python manage.py test module_payment_account
```
该命令将会运行本模块的测试用例, 测试数据在项目中fixtures文件夹下

# TODO
+ 接口暂时未做认证
+ 账户信息查询接口的`view_balance`字段需要查询当前账单,账单模块未完成