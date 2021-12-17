#!/bin/bash

if [ "$FLASK_ENV" == "development" ]; then
    gunicorn --bind "$FLASK_RUN_HOST:$FLASK_RUN_PORT" --worker-connections 2 --threads 4 --reload 'autoscaler:create_app()';
else
    gunicorn --bind "$FLASK_RUN_HOST:$FLASK_RUN_PORT" -w 3 --max-requests 1000 --threads 4 'autoscaler:create_app()';
fi
