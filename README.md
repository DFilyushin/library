# Library #

![favicon-32x32](https://user-images.githubusercontent.com/5266873/57717064-93544b80-76a4-11e9-8371-8b0b49766c5c.png) Web application based on React, Python, Flask for create library by Lib.rus.ec zip-archives.

# About #

Library Librusec is freedom library distributed by zip-archives in torrents. That code created web application for view and download books.
That code processing all zip archives files for extract image with coverpages and additional info. Extracted info put in mongo database for fast access.
Backend code works like REST API service and can use for create bots, web application and other.

# Requirements #

* MongoDB

* Redis

* Python 3.5-3.7 supported.

* Flask 1.11-2.2 suppported.

* NodeJs 10 supported.

* Yarn 1.15

# Install backend #

1. create virtualenv 

2. pip install -r requirements.txt

3. set settings

4. run tools/loader

5. install nginx with ./deploy/library.nginx

6. setup Systemd with ./deploy/library.service
