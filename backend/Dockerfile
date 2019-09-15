FROM python:3.7.2-stretch

WORKDIR /opt/library/backend

ADD . /opt/library/backend

RUN pip install -r requirements.txt

EXPOSE 8080:8080

# CMD ["uwsgi", "/opt/library/backend/app.ini"]
# CMD ["python", "run.py"]
CMD ["./start_server.sh"]