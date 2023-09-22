#!/bin/bash
docker build -t my-chatapp:1 .
docker run -it -v users:/volume my-chatapp:1


