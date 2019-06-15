#!/usr/bin/env bash

echo ">>> Stopping flask containers"
docker stop $( docker ps -a | awk '{ if ($2 == "flask") { print $1 } }' )

echo ">>> Pulling git repository"
cd /home/barycenter/barycenter_repo/
git pull

echo ">>> Building new docker image"
docker build -t flask .

echo ">>> Running new docker image"
docker run -d -p 80:5000 flask

echo ">>> Done"
