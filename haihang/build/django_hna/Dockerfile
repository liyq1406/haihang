FROM payment:base

MAINTAINER YourunCloud "bin.long@youruncloud.com" 

ENV DJANGO_VERSION 1.10.2

COPY ./ /Payment/

RUN echo "Asia/Shanghai" > /etc/timezone && \
    chmod +x /Payment/build/django_hna/run.sh

WORKDIR /Payment

ENTRYPOINT ["/Payment/build/django_hna/run.sh"]