# -*- coding:utf-8 -*-
"""
Django settings for Payment project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from Payment.initConf import ENV_INIT

# Celery settings
# CELERY_BROKER_URL = 'django://'
# CELERY_BROKER_URL = 'redis://192.168.14.5:6379/0'
# CELERY_BROKER_URL = 'redis://120.24.62.88:6379/0'
# BROKER_URL = 'redis://127.0.0.1:6379/0'
# BROKER_TRANSPORT = 'redis'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_TASK_SERIALIZER = 'json'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ub2p6po3ol)1x@^x%p^k(**)_wpuo(33an%8zl!lzhbaz0j#(n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['backend', '127.0.0.1']
ALLOWED_HOSTS = ['backend', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'werkzeug_debugger_runserver',
    # 'django_extensions',
    'rest_framework',
    # 'rest_framework_swagger',
    # 'corsheaders',
    # 'django_celery_results',
    'widget_tweaks',
    'module_payment_account',
    'module_coupon',
    'module_payment',
    'module_reconciliation',
    'cms',
    'bill',
    'price',
    'monitor',
    'statistic',
    'django_crontab',
    'gunicorn',
    'configure',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Payment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Payment.wsgi.application'

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),

    'PAGE_SIZE': 10,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    #     'rest_framework.authentication.TokenAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    # ),

}
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ENV_INIT['MYSQL_DATABASE_NAME'],
        'USER': ENV_INIT['MYSQL_USER'],
        'PASSWORD': ENV_INIT['MYSQL_PASSWORD'],
        'HOST': ENV_INIT['MYSQL_HOST'],
        'PORT': ENV_INIT['MYSQL_PORT'],
        'ATOMIC_REQUESTS': True
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Asia/Shanghai'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_URL = '/cms/login/'
LOGIN_REDIRECT_URL = '/cms/account/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/data/log/payment_debug.log',
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'payment': {
            'handlers': ['file_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
CRONJOBS = [
    # 每月的1号更新月账单定时任务 check_month_account
    ('0 0 1 * *', 'bill.util.month_account', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
    # 每月的2号零点零分去对生成月账单失败的账户重新生成账单
    ('0 0 2 * *', 'bill.cron_check.check_month_account', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
    # 每月一号晚上十一点到凌晨5点每隔两个小时查看月账单支付失败的账单
    ('0 23-6/2 1 * *', 'bill.util.check_fail_accountor', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
    # #额度监控定时任务
    ('0 */2 * * *', 'monitor.util.accountmonitor', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
    # ('* * * * *', 'monitor.util.accountmonitor', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),

    # # paypal对账
    ('0 2 * * *', 'module_reconciliation.tasks.check_paypal', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
    # # alipay对账
    ('0 3 * * *', 'module_reconciliation.tasks.check_alipay', '>>' + BASE_DIR + '/data/log/payment_crontab.log 2>&1'),
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'configure_cache'),
        'TIMEOUT': 180,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

log_dir = os.path.join(BASE_DIR, 'data', 'log')
csv_dir = os.path.join(BASE_DIR, 'data', 'csv')
coupon_dir = os.path.join(BASE_DIR, 'data', 'coupon')
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

if not os.path.isdir(csv_dir):
    os.makedirs(csv_dir)

if not os.path.isdir(coupon_dir):
    os.makedirs(coupon_dir)