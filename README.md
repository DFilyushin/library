# Library #

![favicon-32x32](https://user-images.githubusercontent.com/5266873/57717064-93544b80-76a4-11e9-8371-8b0b49766c5c.png) Web application based on React, Python, Flask for creating FB2 books library from the lib.rus.ec zip-archives.

# About #

The lib.rus.ec is a free library distributed by zip-archives on the torrents. This code creates a web application for viewing and downloading books in the FB2 format.
This code processes all zip-files and extracts coverpages and additional information. Extracted info get stored into the mongo database for fast access.
Back-end code will work as a REST service and can be accessed by bots, web applications, and other services.

# Requirements #

* MongoDB

* Redis

* Python 3.5-3.7 supported.

* Flask 1.11-2.2 suppported.

* NodeJs 10 supported.

* Yarn 1.15

# Install back-end #

1. create virtualenv 

2. pip install -r requirements.txt

3. set settings

4. run tools/loader

5. install nginx with ./deploy/library.nginx

6. setup Systemd with ./deploy/library.service

# Install front-end

1. cd web

2. yarn install

3. yarn build