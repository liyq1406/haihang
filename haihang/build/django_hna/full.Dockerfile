FROM django:1.10.2-python2

MAINTAINER YourunCloud "bin.long@youruncloud.com" 

ENV DJANGO_VERSION 1.10.2

COPY build/django_hna/requirements.txt ./

RUN apt-get update

RUN apt-get install -y python-mysqldb cron

RUN pip install -r requirements.txt

COPY ./ /Payment/

RUN chmod +x /Payment/build/django_hna/run.sh

WORKDIR /Payment

ENTRYPOINT ["/Payment/build/django_hna/run.sh"]