# -*- coding:utf-8 -*-

import types
from urllib import urlencode, urlopen  
from hashcompact import md5_constructor as md5  
from alipayConfig import Settings
    
    
settings = Settings()
 
#字符串编解码处理  
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):  
    if strings_only and isinstance(s, (types.NoneType, int)):  
        return s  
    if not isinstance(s, basestring):  
        try:  
            return str(s)  
        except UnicodeEncodeError:  
            if isinstance(s, Exception):  
                return ' '.join([smart_str(arg, encoding, strings_only,  
                        errors) for arg in s])  
            return unicode(s).encode(encoding, errors)  
    elif isinstance(s, unicode):  
        return s.encode(encoding, errors)  
    elif s and encoding != 'utf-8':  
        return s.decode('utf-8', errors).encode(encoding, errors)  
    else:  
        return s  
    
# 网关地址  
_GATEWAY = 'https://mapi.alipay.com/gateway.do?'  
    
    
# 对数组排序并除去数组中的空值和签名参数  
# 返回数组和链接串  
def params_filter(params):  
    ks = params.keys()  
    ks.sort()  
    newparams = {}  
    prestr = ''  
    for k in ks:  
        v = params[k]  
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)  
        if k not in ('sign','sign_type') and v != '':  
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)  
            prestr += '%s=%s&' % (k, newparams[k])  
    prestr = prestr[:-1]  
    return newparams, prestr  
    
    
# 生成签名结果  
def build_mysign(prestr, key, sign_type = 'MD5'):  
    if sign_type == 'MD5':  
        return md5(prestr + key).hexdigest()  
    return ''  
    
def create_direct_pay_by_alipay(out_trade_no, subject, body, total_fee):  
    """
    alipay即时到账交易接口  
    out_trade_no: 唯一订单号
    subject: 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里
    body: 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里，可以为空
    total_fee: 订单总金额，显示在支付宝收银台里的“应付总额”里，精确到小数点后两位  
    """
    params = {}  
    # 支付宝处理接口名称
    params['service']       = 'create_direct_pay_by_user'  
        
    # 获取配置文件  
    params['partner']           = settings.ALIPAY_PARTNER
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET  
    params['seller_id']         = settings.ALIPAY_PARTNER  
    params['seller_email']      = settings.ALIPAY_SELLER_EMAIL 
    params['payment_type']      = settings.ALIPAY_PAYMENT_TYPE       
      
    params['return_url']        = settings.ALIPAY_RETURN_URL  
    params['notify_url']        = settings.ALIPAY_NOTIFY_URL  
    # params['show_url']          = settings.ALIPAY_SHOW_URL  
    # params['enable_paymethod']  = settings.ALIPAY_ENABLE_PAYMETHOD
    params['goods_type']        = settings.ALIPAY_GOODS_TYPE
    
    # 从订单数据中动态获取到的必填参数  
    params['out_trade_no']  = out_trade_no
    params['subject']       = subject
    params['body']          = body
    params['total_fee']     = total_fee
    
    # 默认支付参数
    # params['paymethod'] = 'directPay'   # 支付方式，四个值可选：bankPay(网银); cartoon(卡通); directPay(余额); CASH(网点支付)  
        
    params,prestr = params_filter(params)  
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)  
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE  
    return _GATEWAY + urlencode(params)  
    
def refund_fastpay_by_platform_pwd(refund_date, batch_no, out_trade_no, total_fee, refund_reason):
    """
    支付宝退款处理接口
    refund_date: 退款时间 格式为：yyyy-MM-dd HH:mm:ss
    batch_no: 退款批次号 格式为：退款日期（8位）+流水号（3～24位）。不可重复，且退款日期必须是当天日期。
              流水号可以接受数字或英文字符，建议使用数字，但不可接受“000”
    out_trade_no: 支付单号
    total_fee: 支付金额
    refund_reason: 退款理由
    """
    params = {}  
    params['service'] = 'refund_fastpay_by_platform_pwd'
    params['partner']           = settings.ALIPAY_PARTNER
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET  
    params['notify_url']        = settings.ALIPAY_REFUND_URL
    params['seller_email']      = settings.ALIPAY_SELLER_EMAIL  
    params['seller_user_id']    = settings.ALIPAY_PARTNER  
    params['refund_date']       = refund_date
    params['batch_no']          = batch_no
    params['batch_num']         = '1'
    params['detail_data']       = '^'.join((out_trade_no,total_fee,refund_reason)) # 原付款支付宝交易号^退款总金额^退款理由

    params,prestr = params_filter(params)  
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)  
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    return _GATEWAY + urlencode(params)    

def alipay_payment_history(page_no, gmt_start_time, gmt_end_time, page_size):
    """
    支付宝历史账单查询
    page_no: 查询页号
    gmt_start_time: 开始时间, 包含该节点
    gmt_end_time: 结束时间,不包含该节点
    page_size: 分页大小, 默认5000
    trans_code: 交易类型, 6001 => 在线支付
    """
    params = {}  
    params['service'] = 'account.page.query'
    params['partner']           = settings.ALIPAY_PARTNER
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET  

    params['page_no'] = page_no
    params['gmt_start_time'] = gmt_start_time
    params['gmt_end_time'] = gmt_end_time
    params['page_size'] = page_size
    # params['trans_code'] = trans_code
    params['trans_code'] = '6001'

    params,prestr = params_filter(params)  
    params['sign'] = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)  
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE
    return _GATEWAY + urlencode(params)    

def notify_verify(post):  
    # 初级验证--签名  
    _,prestr = params_filter(post)  
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)  
    
    if mysign != post.get('sign'):  
        return False  
        
    # 二级验证--查询支付宝服务器此条信息是否有效  
    params = {}  
    params['partner'] = settings.ALIPAY_PARTNER  
    params['notify_id'] = post.get('notify_id')  
    gateway = 'https://mapi.alipay.com/gateway.do?service=notify_verify&'  
    verify_result = urlopen(gateway, urlencode(params)).read()  
    if verify_result.lower().strip() == 'true':  
        return True  
    return False  

def xml_verify(params):
    _,prestr = params_filter(params)  
    mysign = build_mysign(prestr, settings.ALIPAY_KEY, settings.ALIPAY_SIGN_TYPE)  
    if mysign != params.get('sign'):  
        return False  
    return True