import docker

client = docker.from_env()

i = 1

for container in client.containers.list():
    container.stop()
    client.containers.prune(filters=None)
    print("Another victory! ", i)
    i += 1
