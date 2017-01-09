#!/bin/bash

echo "replace start"
swagger=$SWAGGER_UI
sed -i -e 's|somedomain|'$swagger'|' /dist/spec/swagger.yaml
echo "replace complete"

/bin/bash -c "envsubst < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
