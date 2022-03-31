#!/bin/sh

DOCKER_REGISTRY=$1
DOCKER_REGISTRY_USER=$2
DOCKER_REGISTRY_PWD=$3
IMAGE_VERSION=$4

docker login -u $DOCKER_REGISTRY_USER -p $DOCKER_REGISTRY_PWD $DOCKER_REGISTRY

make build USER_ID=$(id -u) GID=$(id -g) VERSION=$IMAGE_VERSION 
if [[ $? != 0 ]]; then
    echo "build image error, please check."
    exit 1
fi
make push VERSION=$IMAGE_VERSION

docker logout $DOCKER_REGISTRY
