#!/bin/bash

docker buildx build --push --platform linux/arm/v7,linux/amd64 --tag gerrowadat/cardblobs:latest .
