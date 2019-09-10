FROM python:3.7.2-stretch

WORKDIR /opt/library

ADD . /opt/library

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]