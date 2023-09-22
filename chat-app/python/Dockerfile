# set base image (host OS)
FROM python:3.8-slim-buster

# Install CA certificates to enable SSL connections
RUN apt-get update && apt-get install -y ca-certificates


WORKDIR /code
#Defines environment variables 
ENV FLASK_ENV development

# Define the environment variables
ENV MYSQL_HOST '192.168.128.1'
ENV MYSQL_USER 'root'
ENV MYSQL_PASSWORD 'pass'
ENV MYSQL_ROOT_PASSWORD 'pass'
ENV MYSQL_PORT '3306'
ENV MYSQL_DATABASE 'chatAppDB'

        
# copy the dependencies file to the working directory
COPY requirements.txt .


# Install the mysql-connector-python package
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt --no-cache-dir


# Install the mysql-connector-python package
# RUN pip install mysql-connector-python

# install curl
RUN apt-get update && apt-get install -y curl

#HEALTHCHECK
HEALTHCHECK --interval=10s --timeout=3s \
CMD curl -fail http://localhost:5000/health || exit 1



# command to run on container start
CMD [ "python", "./chatApp.py" ]
# copy the content of the local src directory to the working directory
COPY . .



