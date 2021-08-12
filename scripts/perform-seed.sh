#!/bin/bash
# ROOT=$(readlink -f $(dirname "$0")/..)

echo "Starting DB Seed"
python manage.py runscript seed
