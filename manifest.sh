#!/bin/bash

gunicorn --reload -w "$GUNICORN_WORKERS" --bind 0.0.0.0:5000 "api:app"