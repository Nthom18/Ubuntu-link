# px4-simulation-docker

Docker files for the PX4 STIL Simulation container

# Building the container

```sh
docker build . -t vm-server[:<tag>]
```

# RUN
```sh
docker run --network host --name vm-server -d -i vm-server[:<tag>] <udp port for mavlink> <gazebo master port>
```

eg.
```sh
docker run --network host --name vm-server -d -i vm-server-1.10.1 16550 17550
```

## Connect to the GZServer (Gazebo GUI)
```sh
GAZEBO_MASTER_URI=http://<ip of the server>:<gazebo master port> gzclient --verbose
```

eg.
```sh
GAZEBO_MASTER_URI=http://localhost:17550 gzclient --verbose
```


## Pushing the container image to Docker Hub

Re-tag an existing local image
```sh
docker tag vm-server[:<tag>] <hub-user>/<repo-name>[:<tag>]
```

Commit the container
```sh
docker commit <existing-container> <hub-user>/<repo-name>
```
