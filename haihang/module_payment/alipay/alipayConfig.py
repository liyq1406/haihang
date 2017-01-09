#-*- coding:utf-8 -*-  

from Payment.initConf import ENV_INIT
from Payment.util import get_config_value

class Settings:  
    # 安全检验码，以数字和字母组成的32位字符  
    public = 'http://' + ENV_INIT['PUBLIC_HOST'] + ':' + ENV_INIT['PUBLIC_PORT'] + '/apis/v1/payments/'
    ALIPAY_KEY = ''  
    ALIPAY_INPUT_CHARSET = 'UTF-8'  
    # 合作身份者ID，以2088开头的16位纯数字  
    ALIPAY_PARTNER = ''  
    # 签约支付宝账号或卖家支付宝帐户  
    ALIPAY_SELLER_EMAIL = ''  
    ALIPAY_SIGN_TYPE = 'MD5'  
    # 付完款后跳转的页面（同步通知） 
    ALIPAY_RETURN_URL= public + 'alipay_return_url/'
    # 交易过程中服务器异步通知的页面
    ALIPAY_NOTIFY_URL= public + 'alipay_notify_url/'
    # 交易退款过程中服务器异步通知的页面
    ALIPAY_REFUND_URL= public + 'alipay_refund_url/'
    # 支付类型, 只支持取值为1（商品购买）
    ALIPAY_PAYMENT_TYPE = '1'
    # 可选支付方式
    ALIPAY_ENABLE_PAYMETHOD = 'directPay^bankPay^cartoon^cash'
    # 虚拟商品
    ALIPAY_GOODS_TYPE = '0'

    # http://112.95.153.98:58000
    
    def __init__(self):
        
        # 安全检验码，以数字和字母组成的32位字符  
        self.ALIPAY_KEY = get_config_value('alipay_key')
        
        # 合作身份者ID，以2088开头的16位纯数字  
        self.ALIPAY_PARTNER = get_config_value('alipay_partner')
        
        # 告警通知邮箱
        self.ALIPAY_SELLER_EMAIL = get_config_value('alipay_seller_email')
        

        
