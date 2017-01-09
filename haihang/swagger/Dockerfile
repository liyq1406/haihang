FROM nginx:alpine

MAINTAINER YourunCloud "bin.long@youruncloud.com" 

USER root
RUN apk add --no-cache bash
# Delete default confs
RUN rm -rf /etc/nginx/conf.d/*.conf

# Copy our confs to image
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

RUN chmod +x /etc/nginx/conf.d/config.sh

# Add dist.tar to image
ADD dist.tar /
# copy swagger.yaml
COPY spec/ /dist/spec/

#Replace env
ENTRYPOINT ["/etc/nginx/conf.d/config.sh"]
