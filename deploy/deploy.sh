#!/bin/sh

library="/var/www/library"
service="library.service"
frontend="/var/www/library/web"
webuser="www-data"
venv="/var/www/library/venv/bin/python"

git pull origin

rsync --exclude '*_settings.py'  ./*.py ${library}
rsync ./storage/*.py ${library}/storage/
rsync ./tools/*.py ${library}/tools/
rsync ./endpoints/*.py ${library}/endpoints/
rsync ./models/*.py ${library}/models/

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

