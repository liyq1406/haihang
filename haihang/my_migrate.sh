#! /bin/sh
echo "=============> 删除migrations"
rm -rf bill/migrations/
rm -rf price/migrations/ 
rm -rf statistic/migrations/ 
rm -rf monitor/migrations/ 
rm -rf module_coupon/migrations/ 
rm -rf module_payment/migrations/ 
rm -rf module_payment_account/migrations/ 
rm -rf module_reconciliation/migrations/ 
echo "=============> makemigrations"
python manage.py  migrate
python manage.py  makemigrations bill
python manage.py  makemigrations price
python manage.py  makemigrations monitor
python manage.py  makemigrations statistic
python manage.py  makemigrations module_payment
python manage.py  makemigrations module_coupon
python manage.py  makemigrations module_payment_account
python manage.py  makemigrations module_reconciliation
python manage.py makemigrations configure
echo "=============> migrate"
python manage.py  migrate
echo "=============> end"
# python manage.py createsuperuser