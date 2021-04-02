#!/bin/bash

docker buildx build --push --platform linux/arm/v7,linux/amd64,linux/arm64 --tag gerrowadat/playerbot:latest .
