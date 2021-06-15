'''
Management of containers and init of offboard control and appliance of behaviour.

Author: Nicoline Louise Thomsen
'''

import subprocess
import time
import tkinter

import offb_posctl as offb

from drone import Drone

from kinematic_simulation_copy.behaviour import Behaviour
import kinematic_simulation_copy.constants as constants

SWARM_SIZE = 5
docker_wait = 4

def start_drones_d():

    x = 0
    y = -2.5

    drone_containers.append("sdu_drone_0")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 0 " + str(x-1) + " " + str(y)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

    drone_containers.append("sdu_drone_1")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 1 " + str(x+1) + " " + str(y)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

    drone_containers.append("sdu_drone_2")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 2 " + str(x-1) + " " + str(y-2)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

    drone_containers.append("sdu_drone_3")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 3 " + str(x+1) + " " + str(y-2)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

    drone_containers.append("sdu_drone_4")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 4 " + str(x) + " " + str(y-1)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

def start_drones_1():
    x = 0
    y = -2.5

    drone_containers.append("sdu_drone_0")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 0 " + str(x-1) + " " + str(y)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

def start_drones_2():
    x = 0
    y = -2.5

    drone_containers.append("sdu_drone_0")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 0 " + str(x-1) + " " + str(y)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

    drone_containers.append("sdu_drone_1")
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 1 " + str(x+1) + " " + str(y)
    subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    time.sleep(docker_wait)

# Start containers
print("--- Starting containers ---")
print('\n')

bashCmd = "docker run --name world --network host -id --rm vm-server-sdu-world-custom 17550 11311 case_d"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# output, error = process.communicate()
time.sleep(docker_wait)

drone_containers = []


start_drones_d()
# start_drones_1()
# start_drones_2()


print("Drone containers: ", drone_containers)

# Starting simulation
print('\n')
print("--- Starting simulation ---")
print('\n')

# Initiate OFFBOARD CONTROL for all drone containers
drone_controls = [offb.OffboardControl(container) for container in drone_containers]
flock = [Drone(drone_controllers, id) for id, drone_controllers in enumerate(drone_controls)]

time.sleep(15)   # Let last drone get airborne

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

# MAIN LOOP ###################################
while btn['state'] == tkinter.NORMAL:

    rule_picker = (rule_picker + 1) % 2

    for drone in flock:

        steer.update(drone, flock, target, rule_picker)  # Steering vector
        drone.update(steer.force)


    root.update_idletasks()
    root.update()
    time.sleep(0.01)





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



print('\n')
print("--- Shutdown initiating ---")
print('\n')

# Stop offboard commands
print("1/3) Stopping offboard commands...")
print('\n')
for i in range(SWARM_SIZE):
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

drone_container_list = ""
for container in drone_containers:
    drone_container_list += " " + str(container)

bashCmd = "docker stop world" + drone_container_list
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
output, error = process.communicate()

print('\n')
print("--- DONE ---")

