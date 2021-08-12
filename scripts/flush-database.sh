#!/bin/bash
# ROOT=$(readlink -f $(dirname "$0")/..)

echo "Flushing database..." 
python manage.py flush --skip-checks --no-input
echo "Flush complete"
