#!/usr/bin/env bash

if [[ "$APP_DEBUG" == "true" ]]
then
	echo "Starting development server on port 6000..."
	exec python manage.py runserver 0.0.0.0:6000
else
	if [[ "$RUN_TYPE" == "sockfile" ]]
	then
		echo "Starting production server on socket file run/connection.sock..."
		bind_target="unix:run/connection.sock"
	elif [[ "$RUN_TYPE" == "server" ]]
	then
		echo "Starting production server on port 6000..."
		bind_target=0.0.0.0:6000
	else
		echo "Invalid value for RUN_TYPE env variable" 
		echo "Expected values: \`server\` or \`sockfile\` "
		echo "Received value: $RUN_TYPE"
		exit 1
	fi

	bootstap_name=app.bootstrap

	exec env DJANGO_SETTINGS_MODULE=${bootstap_name}.settings \
		gunicorn ${bootstap_name}.wsgi:application \
			--name "GunicornApp" \
			--workers $RUN_WORKERS \
			--user="www-data" --group="www-data" \
			--bind=${bind_target} \
			--log-level=info \
			--log-file=-
fi