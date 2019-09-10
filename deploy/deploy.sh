#!/bin/sh

library="/var/www/library"
service="library.service"
frontend="/var/www/library/web"
webuser="www-data"
venv="/var/www/library/venv/bin/python"

git pull origin

rsync --exclude '*_settings.py'  ./backend/*.py ${library}
rsync ./backend/storage/*.py ${library}/storage/
rsync ./backend/tools/*.py ${library}/tools/
rsync ./backend/endpoints/*.py ${library}/endpoints/
rsync ./backend/models/*.py ${library}/models/

chown -R ${webuser}:${webuser} ${library}/

cd ./web/

yarn install
yarn build

# copy frontend to web-dir & set access right to webuser
cp -R ./build ${frontend}
chown -R ${webuser}:${webuser} ${frontend}/


# reload cache
${venv} /var/www/library/cache_reload.py


# restart service & check state
systemctl restart ${service}
systemctl -q is-active ${service}  && echo "Library Running" || echo "Service is not running"

