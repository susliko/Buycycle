#!/usr/bin/env bash
rsync -r --delete-after --quiet $TRAVIS_BUILD_DIR/ root@$SERVER_ADDR:/home/buycycle
ssh buycycle@$SERVER_ADDR 'mkdir /home/buycycle/buycycle/logs'
ssh root@$SERVER_ADDR 'pip3 install -r /opt/buycycle/requirements.txt'
ssh root@$SERVER_ADDR 'systemctl restart gunicorn'