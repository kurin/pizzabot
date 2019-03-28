#!/bin/sh

set -ex

docker-compose down
docker-compose build
docker-compose up -d
docker-compose exec foodbrowser npm run bundle
docker cp app_foodbrowser_1:/usr/src/app/bundle.js dist/
docker cp app_foodbrowser_1:/usr/src/app/index.html dist/
git rev-parse HEAD > dist/version.txt
docker-compose down
if [[ `hostname` = 'sometimes.org' ]]; then
  cp ./dist/* /var/www/html/talkingpizza/foodbrowser/
fi
