#! /bin/sh
gunicorn Payment.wsgi:application -b 127.0.0.1:8000
