'''
Management of containers and init of offboard control and appliance of behaviour.

Author: Nicoline Louise Thomsen
'''

import docker
import subprocess
import time
import tkinter

import offb_posctl as offb

from docker_init import Docker_init
from drone import Drone

from kinematic_simulation_copy.behaviour import Behaviour
import kinematic_simulation_copy.constants as constants

SWARM_SIZE = 5
docker_wait = 4


def start_containers_d():
    client.containers.run('vm-server-sdu-world-custom', '17550 11311 case_d', 
                        name='world', 
                        network='host',
                        detach=True, 
                        remove=True,
                        # restart_policy={"Name": "on-failure", "MaximumRetryCount": 1}
                        )

    x = 0
    y = -2.5
    
    client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 0 ' + str(x-1) + " " + str(y), 
                        name='sdu_drone_0', 
                        network='host',
                        detach=True, 
                        remove=True,
                        # restart_policy={"Name": "on-failure", "MaximumRetryCount": 1}
                        )

    # client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 1 ' + str(x+1) + " " + str(y), 
    #                     name='sdu_drone_1', 
    #                     network='host',
    #                     detach=True, 
    #                     # remove=True,
    #                     restart_policy={"Name": "on-failure", "MaximumRetryCount": 1})

    # client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 2 ' + str(x-1) + " " + str(y-2), 
    #                     name='sdu_drone_2', 
    #                     network='host',
    #                     detach=True, 
    #                     # remove=True,
    #                     restart_policy={"Name": "on-failure", "MaximumRetryCount": 1})

    # client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 3 ' + str(x+1) + " " + str(y-2), 
    #                     name='sdu_drone_3', 
    #                     network='host',
    #                     detach=True, 
    #                     # remove=True,
    #                     restart_policy={"Name": "on-failure", "MaximumRetryCount": 1})

    # client.containers.run('sduuascenter/px4-simulation:vm-server-sdu-drone', '16550 17550 11311 sdu_drone 4 ' + str(x) + " " + str(y-1), 
    #                     name='sdu_drone_4', 
    #                     network='host',
    #                     detach=True, 
    #                     # remove=True,
    #                     restart_policy={"Name": "on-failure", "MaximumRetryCount": 1})

drone_containers = []
drone_containers.append("sdu_drone_0")
# drone_containers.append("sdu_drone_1")
# drone_containers.append("sdu_drone_2")
# drone_containers.append("sdu_drone_3")
# drone_containers.append("sdu_drone_4")

##################### Starting containers #####################

print("--- Starting containers ---")
print('\n')

client = docker.from_env()
start_containers_d()


print("Drone containers: ", drone_containers)

##################### Starting simulation #####################
print('\n')
print("--- Starting simulation ---")
print('\n')

# Initiate OFFBOARD CONTROL for all drone containers
drone_controls = [offb.OffboardControl(container) for container in drone_containers]
flock = [Drone(drone_controllers, id) for id, drone_controllers in enumerate(drone_controls)]

# time.sleep(15)   # Let last drone get airborne

print('\n')
print("--- Startup complete ---")


# Tkinter windown for shutdown (hover over button)
root = tkinter.Tk()
root.resizable(width = False, height = False)
btn = tkinter.Button(root, text = 'Initiate shutdown', bd = '5')
btn.pack()


case_id = 'd'
rule_picker = 0
target = [0, -(864 - 100) * constants.GAZEBO_SCALE]   # Same goal as kinematic after rescaling 
steer = Behaviour(case_id)   # Steering vector


##################### MAIN LOOP #####################

while btn['state'] == tkinter.NORMAL:

    rule_picker = (rule_picker + 1) % 2

    for drone in flock:

        steer.update(drone, flock, target, rule_picker)  # Steering vector
        drone.update(steer.force)


    root.update_idletasks()
    root.update()
    time.sleep(0.01)

#####################################################



# Test service calls

# bashCmd = "rosservice call /setpoint_controller/circle {{}}"
# process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# time.sleep(10)


# bashCmd = "rosservice call /setpoint_controller/forward" + str(0)
# process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# bashCmd = "rosservice call /setpoint_controller/backward" + str(1)
# process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# time.sleep(10)

# print(drone_controls[0].target)


##################### Shutdown sequence #####################


print('\n')
print("--- Shutdown initiating ---")
print('\n')

# Stop offboard commands
print("1/3) Stopping offboard commands...")
print('\n')
for i in range(len(drone_containers)):
    bashCmd = "rosservice call /setpoint_controller/stop" + str(i)
    process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
time.sleep(5)

# Stop ROS
print('\n')
print("2/3) Shutting down ROS...")
print('\n')
for control in drone_controls:
    control.shutdown()

# Stop containers
print('\n')
print("3/3) Shutting down containers...")

for container in client.containers.list():
    container.stop()

print('\n')
print("--- DONE ---")

