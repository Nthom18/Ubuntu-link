import docker
import time

class Docker_init():

    def __init__(self, docker_client, nr_of_drones = 1):

        self.client = docker_client

        # Create drone container list
        self.container_list = ['world']

        for id in range(nr_of_drones):
            self.container_list.append('sdu_drone_' + str(id))
            # self.container_list.append('world' + str(id))

        self.containers()


    def containers(self):
        
        def missing_containers():
            running_container = self.client.containers.list()
            created_containers = [container.name for container in running_container]

            return list(set(self.container_list) - set(created_containers))

        def create_containers(missing_containers):
            for container in missing_containers:
                # CREATE DOCKER CONTAINER
                if container == 'world':
                    client.containers.run('vm-server-sdu-world-custom', '17550 11311 case_d', 
                        name=container, 
                        network='host',
                        detach=True, 
                        remove=True)

                else:
                    client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 0 0 0', 
                        name=container, 
                        network='host',
                        detach=True, 
                        remove=True)

        
        while(len(missing_containers()) != 0):
            create_containers(missing_containers())
            time.sleep(3)



if __name__ == '__main__':

    client = docker.from_env()

    foo = Docker_init(client, 10)

    # for container in client.containers.list():
    #     container.stop()
        

