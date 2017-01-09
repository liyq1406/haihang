#!/bin/bash

echo "===================> set ENV"
sed -i -e "s|'MYSQL_USER': 'MYSQL_USER',|'MYSQL_USER': '$MYSQL_USER',|" /Payment/Payment/initConf.py
sed -i -e "s|'MYSQL_PASSWORD': 'MYSQL_PASSWORD',|'MYSQL_PASSWORD': '$MYSQL_PASSWORD',|" /Payment/Payment/initConf.py
sed -i -e "s|'MYSQL_DATABASE_NAME': 'MYSQL_DATABASE_NAME',|'MYSQL_DATABASE_NAME': '$MYSQL_DATABASE_NAME',|" /Payment/Payment/initConf.py
sed -i -e "s|'MYSQL_HOST': 'MYSQL_HOST',|'MYSQL_HOST': '$MYSQL_HOST',|" /Payment/Payment/initConf.py
sed -i -e "s|'MYSQL_PORT': 'MYSQL_PORT',|'MYSQL_PORT': '$MYSQL_PORT',|" /Payment/Payment/initConf.py
sed -i -e "s|'PUBLIC_HOST': 'PUBLIC_HOST',|'PUBLIC_HOST': '$PUBLIC_HOST',|" /Payment/Payment/initConf.py
sed -i -e "s|'PUBLIC_PORT': 'PUBLIC_PORT',|'PUBLIC_PORT': '$PUBLIC_PORT',|" /Payment/Payment/initConf.py
sed -i -e "s|'RANCHER_URL': 'RANCHER_URL',|'RANCHER_URL': '$RANCHER_URL',|" /Payment/Payment/initConf.py
sed -i -e "s|'REDIS_HOST': 'REDIS_HOST',|'REDIS_HOST': '$REDIS_HOST',|" /Payment/Payment/initConf.py
sed -i -e "s|'REDIS_PORT': 'REDIS_PORT',|'REDIS_PORT': '$REDIS_PORT',|" /Payment/Payment/initConf.py
sed -i -e "s|'REDIS_DB': 'REDIS_DB',|'REDIS_DB': '$REDIS_DB',|" /Payment/Payment/initConf.py
sed -i -e "s|'ALERT_URL': 'ALERT_URL',|'ALERT_URL': '$ALERT_URL',|" /Payment/Payment/initConf.py
sed -i -e "s|'API_KEY': 'API_KEY',|'API_KEY': '$API_KEY',|" /Payment/Payment/initConf.py
sed -i -e "s|'API_PASS': 'API_PASS',|'API_PASS': '$API_PASS',|" /Payment/Payment/initConf.py
sed -i -e "s|'USER_SYSTEM_URL': 'USER_SYSTEM_URL',|'USER_SYSTEM_URL': '$USER_SYSTEM_URL',|" /Payment/Payment/initConf.py

# echo "===================> create defult user"
# expect << EOF
# spawn python manage.py createsuperuser
# sleep 1
# expect "*Username:"
# send "hna_admin\r"
# sleep 1
# expect "*Email address:"
# send "qin.liu1@hnair.com\r"
# sleep 1
# expect "*Password:"
# send "Ab12345Z\r"
# sleep 1
# expect "*Password (again):"
# send "Ab12345Z\r"
# expect eof
# EOF


if [ $IS_MASTER == 1 ];then
    echo "===================> add tasks"
    python manage.py crontab add
    /etc/init.d/cron restart
    crontab -l
else
    echo "===================> the server is slave"
fi


echo "===================> start app"
gunicorn Payment.wsgi:application -b 0.0.0.0:8000
