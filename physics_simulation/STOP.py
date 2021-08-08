import docker

client = docker.from_env()
client.containers.prune(filters=None)

print('Stopping the', len(client.containers.list()), 'running containers...', '\n')

for container in client.containers.list():
    container.stop()
    client.containers.prune(filters=None)
    print(container.name)

print('\n', '...Done')
