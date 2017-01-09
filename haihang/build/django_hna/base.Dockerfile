FROM django:1.10.2-python2

MAINTAINER YourunCloud "bin.long@youruncloud.com" 

ENV DJANGO_VERSION 1.10.2

COPY requirements.txt ./

RUN set -x
    && apt-get update && apt-get install -y libffi-dev gcc python-mysqldb cron --no-install-recommends \ 
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc


