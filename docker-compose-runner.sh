#!/usr/bin/env bash

project_name="spell-erp"

if [[ "$1" == "--prod" ]]
then
    exec env DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 \
        docker-compose \
        -p "${project_name}-prod" \
        "${@:2}"
else
    exec env DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose \
        -f docker-compose.dev.yaml \
        -p "${project_name}-dev" \
        "$@"
fi