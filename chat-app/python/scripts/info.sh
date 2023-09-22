#!/bin/bash

# Get all the containers
containers=$(docker ps -a)

# Get all the images
images=$(docker images)

# Get all the volumes
volumes=$(docker volume ls)

# Get all the networks
networks=$(docker network ls)

# Print the containers
echo "Containers:"
echo "$containers"

# Print the images
echo "Images:"
echo "$images"

# Print the volumes
echo "Volumes:"
echo "$volumes"

# Print the networks
echo "Networks:"
echo "$networks"


#This will print all the containers, images, volumes, and networks docker is using.prune