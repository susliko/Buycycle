#!/usr/bin/env bash
rsync -r --delete-after --quiet $TRAVIS_BUILD_DIR/ root@$SERVER_ADDR:/opt/buycycle
ssh root@$SERVER_ADDR 'mkdir /opt/buycycle/buycycle/logs'
ssh root@$SERVER_ADDR 'systemctl restart gunicorn'