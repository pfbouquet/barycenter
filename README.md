Welcome!


How to?


# Connect to VM
gcloud compute --project "calcium-complex-121611" ssh --zone "europe-west3-b" "cn-smart-meeting-place"

## Run a docker container for the Python code
docker run -d -p 5432:5432 --name smart-meeting-place-postgres -e POSTGRES_PASSWORD=postgres postgres

Check that the container is running
`docker ps`

Go inside the docker
`docker exec -it smart-meeting-place-postgres bash`

# Connect to SQL database
Setup a Cloud SQL DataBase PostgreSQL
Instance here: https://console.cloud.google.com/sql/instances/bbc-codingnight-smart-meeting-place/overview?project=calcium-complex-121611&duration=PT1H
Instance id: `bbc-codingnight-smart-meeting-place`
`gcloud sql connect bbc-codingnight-smart-meeting-place --user=postgres`

# First initialization of VM
Ask a static external IP

## Install Git on Debian
See here: https://docs.docker.com/install/linux/docker-ce/debian/

## Clone repo
```git clone https://github.com/raphaelberly/smart-meeting-place.git```

## Install Docker

`sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common`

`curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -`

`sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"`

`sudo apt-get update`

`sudo apt-get install docker-ce docker-ce-cli containerd.io`

`sudo docker build -t image_name .`


# First initialization of Cloud SQL PostGreSQL
Open access to all ips (not secure): 0.0.0.0/0
`CREATE EXTENSION POSTGIS;`
 
Create a db for the project
`CREATE DATABASE smart_meeting_place;`

Check that db is indeed created
`\l`

`sudo docker build -t flask .`

By PF, Raphaël, Clément, Hugo