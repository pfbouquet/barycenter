# Run a docker container
docker run -d -p 5432:5432 --name smart-meeting-place-postgres -e POSTGRES_PASSWORD=postgres postgres

# check that the container is running
docker ps

# Go inside the docker
docker exec -it smart-meeting-place-postgres bash

# access postgre
psql -U postgres

# Create a db for the project
CREATE DATABASE smart_meeting_place;

# Check that db is indeed created
\l
