
#!/bin/bash

# Get the version from the user
echo "Enter the version to delete:"
read version

# Stop and remove the Docker container with the provided version
docker stop $(docker ps -q --filter "ancestor=my-chatapp:${version}")
docker rm $(docker ps -aq --filter "ancestor=my-chatapp:${version}")

# Remove the Docker image with the provided version
docker rmi my-chatapp:${version}
