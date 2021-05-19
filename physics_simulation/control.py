"""
Management of containers and, init of offboard control and appliance of behaviour.

Author: Nicoline Louise Thomsen
"""

import subprocess
import threading
import time
import tkinter

import offb_posctl as offb

from kinematic_simulation_copy.behaviour import Behaviour
from drone import Drone
import kinematic_simulation_copy.constants
from kinematic_simulation_copy.logger import Logger
from kinematic_simulation_copy.vector import Vector2D


SWARM_SIZE = 2

# Start containers
print("--- Starting containers ---")
print('\n')

bashCmd = "docker run --name world --network host -id --rm sduuascenter/px4-simulation:vm-server-sdu-world 17550 11311 empty"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# output, error = process.communicate()
time.sleep(3)

drone_containers = []

for i in range(SWARM_SIZE):
    drone_containers.append("sdu_drone_" + str(i))
    bashCmd = "docker run --name " + drone_containers[-1] + " --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone " + str(i) + " 0 " + str(i)
    process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
    # output, error = process.communicate()
    time.sleep(3)

print("Drone containers: ", drone_containers)

# Starting simulation
print('\n')
print("--- Starting simulation ---")
print('\n')

# Initiate OFFBOARD CONTROL for all drone containers
drone_controls = [offb.OffboardControl(container) for container in drone_containers]
flock = [Drone(drone_controllers, id) for id, drone_controllers in enumerate(drone_controls)]

print('\n')
print("--- Startup complete ---")


# Tkinter windown for shutdown - PAUSES PROGRAM UNTIL BUTTON PRESS (hover over button)
root = tkinter.Tk()
root.resizable(width = False, height = False)
btn = tkinter.Button(root, text = 'Initiate shutdown', bd = '5')
btn.pack()


steer = Behaviour()   # Steering vector


while btn['state'] == tkinter.NORMAL:







    root.update_idletasks()
    root.update()
    time.sleep(0.01)








# # Test service call
# for i in range(SWARM_SIZE):
#     bashCmd = "rosservice call /setpoint_controller/forward" + str(i)
#     process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
# time.sleep(10)

bashCmd = "rosservice call /setpoint_controller/forward" + str(0)
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
bashCmd = "rosservice call /setpoint_controller/backward" + str(1)
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
time.sleep(10)

print(drone_controls[0].target)



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
