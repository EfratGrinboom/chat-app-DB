#!/bin/bash

echo "Pruning containers..."
docker container prune -f

echo "Pruning images..."
docker image prune -a -f

echo "Pruning volumes..."
docker volume prune -f

echo "Pruning networks..."
docker network prune -f

echo "Pruning completed."
