#!/bin/bash

. settings/env.cfg
bash db.sh create-db
gunicorn --reload -w "$GUNICORN_WORKERS" --bind 0.0.0.0:5000 "api:app"