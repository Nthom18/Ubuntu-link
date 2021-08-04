import docker
import time

# Docker deamon connected by the default soscket
client = docker.from_env()

client.containers.run('vm-server-sdu-world-custom', '17550 11311 case_d', 
                    #   name='world', 
                      network='host',
                      detach=True, 
                    #   remove=True,
                      restart_policy={"Name": "on-failure", "MaximumRetryCount": 5})

client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 0 0 0', 
                    #   name='drone', 
                      network='host',
                      detach=True, 
                    #   remove=True,
                      restart_policy={"Name": "on-failure", "MaximumRetryCount": 5})


time.sleep(10)
print("stopping")


for container in client.containers.list():
    container.stop()

