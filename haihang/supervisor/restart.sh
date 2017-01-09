# !/usr/bin
# rm -rf *.log
touch payment_beat.log
touch payment_worker.log
sudo supervisorctl restart payment_celery_worker
sudo supervisorctl restart payment_celery_beat