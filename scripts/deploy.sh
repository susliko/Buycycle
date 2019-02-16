#!/usr/bin/env bash
rsync -r --delete-after --quiet $TRAVIS_BUILD_DIR/ root@$SERVER_ADDR:/opt/buycycle
