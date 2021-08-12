#!/bin/bash
# ROOT=$(readlink -f $(dirname "$0")/..)

echo "Flushing database..." 
echo "yes" | python manage.py reset_db > /dev/null
echo "Flush complete"

MIGRATIONS_SUBFOLDER=$(./scripts/getconfig.py main.migration_branch_name)

echo "Starting fresh database migration..."
rm -rf ./migrations/${MIGRATIONS_SUBFOLDER}/*
mkdir -p ./migrations/${MIGRATIONS_SUBFOLDER}
touch ./migrations/${MIGRATIONS_SUBFOLDER}/__init__.py

python manage.py makemigrations
python manage.py migrate

if [[ "$1" == "--seed" ]]; then
    echo "Seeding..."
    python manage.py runscript seed
    echo "Seeding complete"
fi
