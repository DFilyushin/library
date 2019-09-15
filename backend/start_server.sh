#!/bin/bash

if [ -z "$RUN_COMMAND" ]
then
      echo "No set command to execute"
else
      echo "\$FLASK_ENV is NOT empty"
      if [ ${RUN_COMMAND} == "server" ]
      then
        echo "Starting server..."
        uwsgi /opt/library/backend/app.ini
      elif [ ${RUN_COMMAND} == "update" ]
      then
        echo "Updating database..."
        python loader.py
      fi
fi
