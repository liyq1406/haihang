FROM nginx:alpine

MAINTAINER YourunCloud "bin.long@youruncloud.com"

USER root
RUN apk add --no-cache bash
# Delete default confs
RUN rm -rf /etc/nginx/conf.d/*.conf

# Copy our confs to image
COPY build/gunicorn_nginx/nginx.conf /etc/nginx/nginx.conf
COPY build/gunicorn_nginx/conf.d/ /etc/nginx/conf.d/
COPY static/ /payment/static
RUN chmod +x /etc/nginx/conf.d/config.sh

#Replace env
ENTRYPOINT ["/etc/nginx/conf.d/config.sh"]