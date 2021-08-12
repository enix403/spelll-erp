#!/usr/bin/env bash

MIGRATIONS_SUBFOLDER=$(./scripts/getconfig.py main.migration_branch_name)

# create empty directories for expected volumes folder to
# make sure the app still works even if the external
# persistent volumes are not mounted 
mkdir -p \
	run \
	storage/{assets,logs,sessions} \
	migrations/${MIGRATIONS_SUBFOLDER}

touch migrations/${MIGRATIONS_SUBFOLDER}/__init__.py

# wait for mysql server to come live
./scripts/wait-for-it.sh \
	${DB_HOST}:${DB_PORT} \
	--strict \
	--timeout=500 \
	-- ./scripts/start_app.sh

