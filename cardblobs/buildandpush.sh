#!/bin/bash

docker buildx build --push --platform linux/arm/v7,linux/amd64,linux/arm64 --tag docker-registry.home.andvari.net:5000/cardblobs:latest .
