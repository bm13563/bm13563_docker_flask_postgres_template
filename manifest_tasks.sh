#!/bin/bash

celery -A tasks worker --loglevel=INFO &
python3 scheduler/scheduler.py
