#-*- coding:utf-8 -*-

from Payment.initConf import ENV_INIT
from Payment.util import get_config_value

class Settings:
    # 运行模式, sandbox live
    public = 'http://' + ENV_INIT['PUBLIC_HOST'] + ':' + ENV_INIT['PUBLIC_PORT'] + '/apis/v1/payments/'
    MODE = ''
    # 客户端ID
    CLIENT_ID = ''
    # 客户端密匙
    CLIENT_SECRET = ''
    # paypal 订单确认回调接口
    RETURN_URL = public + 'paypal_return_url/'
    # paypal 订单取消回调接口
    CANCEL_URL = public + 'paypal_cancel_url/'
    # paypal 订单webhook回调接口
    # WEBHOOK_URL = 'https://www.jialiao88.com:58000/apis/v1/payments/paypal_webhook_url/'
    
    
    def __init__(self):
        
        # 客户端ID
        self.MODE = get_config_value('paypal_mode')
        
        # 客户端密钥
        self.CLIENT_ID = get_config_value('paypal_client_id')
        
        # 客户端密匙
        self.CLIENT_SECRET = get_config_value('paypal_client_secret')
