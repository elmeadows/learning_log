#!/bin/bash

# Run migration
python manage.py migrate

# Start gunicorn
gunicorn learning_log.wsgi:application