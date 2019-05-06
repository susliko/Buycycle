#!/usr/bin/env bash
rsync -r --delete-after --quiet $TRAVIS_BUILD_DIR/ buycycle@$SERVER_ADDR:/home/buycycle/project
ssh buycycle@$SERVER_ADDR 'mkdir /home/buycycle/project/buycycle/logs'
ssh root@$SERVER_ADDR 'pip3 install -r /home/buycycle/project/requirements.txt'
ssh root@$SERVER_ADDR 'systemctl restart gunicorn'