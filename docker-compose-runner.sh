#!/usr/bin/env bash

if [[ "$1" == "--prod" ]]
then
    exec env DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 \
        docker-compose \
        -p "spell-erp-prod" \
        "${@:2}"
else
    exec env DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose \
        -f docker-compose.dev.yaml \
        -p "spell-erp-dev" \
        "$@"
fi