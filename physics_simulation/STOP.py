import docker

client = docker.from_env()
client.containers.prune(filters=None)

i = 1

for container in client.containers.list():
    container.stop()
    client.containers.prune(filters=None)
    print("Another victory! ", i)
    i += 1


