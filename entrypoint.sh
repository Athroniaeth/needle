#!/bin/bash

# Replace variables in the template
envsubst '${DOMAIN} ${ENVIRONMENT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Start Nginx
exec nginx -g 'daemon off;'
