#!/bin/bash

docker stop nadia
docker rm nadia
docker rmi nadia
git pull origin master
docker build -t nadia .
docker run -d --restart always --name nadia -p 80:80 -v /home/nadia/gallery:/app/static/gallery nadia