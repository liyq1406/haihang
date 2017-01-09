# -*- coding:utf-8 -*-

from Payment.initConf import ENV_INIT
from functools import wraps
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
import logging
import requests

log = logging.getLogger('payment')


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


def auth_required(role=None):
    """
    鉴权接口, 默认鉴权级别 admin
    role: 鉴权角色， superadmin, admin
    HTTP_ROLE_AUTH: 请求头角色信息
    """
    role = 'superadmin' if (role is None) else role

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
#            try:
#                cookie = args[1].META.get('HTTP_COOKIE', None)
#                user_system_url = ENV_INIT['USER_SYSTEM_URL']
#                res = requests.get(user_system_url, timeout=10, headers={'cookie': cookie}).json()
#                if res.get('code') != '200':
#                    return Response({
#                        'detail': '认证失败',
#                        'error_code': '8401'
#                    }, status.HTTP_401_UNAUTHORIZED)
#                role_auth = res.get('data',{}).get('role')
#                if (role == 'superadmin' and role_auth != '0') or (role == 'admin' and role_auth not in ('1', '0')):
#                    return Response({
#                        'detail': '权限不足',
#                        'error_code': '8403'
#                    }, status.HTTP_403_FORBIDDEN)
#            except requests.RequestException as e:
#                log.error('visit %s error', user_system_url)
#                return Response({
#                    'detail': '鉴权错误',
#                    'error_code': '8500'
#                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#            except Exception as e:
#                log.error(e)
#                return Response({
#                    'detail': '内部错误',
#                    'error_code': '8500'
#                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # 认证以及鉴权成功，执行具体业务逻辑
            return func(*args, **kwargs)
        return wrapper
    return decorator
