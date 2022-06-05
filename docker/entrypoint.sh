#!/usr/bin/env bash
# https://medium.com/google-cloud/cloud-run-multiple-processes-4b6f1b3827e
set -e

printenv

HOST=0.0.0.0 PORT=4001 node /app/app/build/index.js &

cd /app/api
python3 -m uvicorn api.app:app --host 0.0.0.0 --port 4002 &
cd -

# wait before we start nginx
while nc -z localhost 4001; do sleep 0.1; done
while nc -z localhost 4002; do sleep 0.1; done

cp /app/nginx/nginx-cloudrun.conf /etc/nginx/conf.d/default.conf
nginx -g "daemon off;" &
echo "running proxy on http://localhost:8080"

wait -n
