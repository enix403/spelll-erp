#!/usr/bin/env bash

image_name="spell-erp/spell-erp-image"


if [[ "$1" == '--help' ]]
then
    echo "Usage: BuildAppImage [--tag TAG]"
    exit 0
elif [[ "$1" == '--tag' ]]
then
    if [[ -z "$2" ]]
    then
        echo "Invalid tag"
        exit 1
    else
        exec env DOCKER_BUILDKIT=1 docker build -f build.dockerfile -t "${image_name}:$2" .
    fi
else
    exec env DOCKER_BUILDKIT=1 docker build -f build.dockerfile -t ${image_name} .
fi
