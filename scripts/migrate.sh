#!/bin/bash
# ROOT=$(readlink -f $(dirname "$0")/..)
python manage.py makemigrations
python manage.py migrate
