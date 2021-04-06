"""
Management of containers and, init of offboard control and appliance of behaviour.

Author: Nicoline Louise Thomsen
"""

import subprocess
import threading
import time
import tkinter

import offb_posctl as offb

# Start containers
print("--- Starting containers ---")

bashCmd = "docker run --name world --network host -id --rm sduuascenter/px4-simulation:vm-server-sdu-world 17550 11311 empty"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
output, error = process.communicate()
time.sleep(2)

bashCmd = "docker run --name drone --network host --rm -id sduuascenter/px4-simulation:vm-server-sdu-drone 16550 17550 11311 sdu_drone 1 -1 -1"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
output, error = process.communicate()
time.sleep(2)

# Starting simulation
print('\n')
print("--- Starting simulation ---")

# Initiate OFFBOARD CONTROL
SPC = offb.OffboardControl()

print('\n')
print("--- Startup complete ---")



# Tkinter windown for shutdown - PAUSES PROGRAM UNTIL BUTTON PRESS
root = tkinter.Tk()
root.resizable(width = False, height = False)
btn = tkinter.Button(root, text = 'Terminate program', bd = '5', command = root.destroy)
btn.pack()
root.mainloop()



# Test service call
bashCmd = "rosservice call /setpoint_controller/forward"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
time.sleep(10)



print('\n')
print("--- Shutdown initiating ---")
print('\n')

# Stop offboard commands
print("1/3) Stopping offboard commands...")
print('\n')
bashCmd = "rosservice call /setpoint_controller/stop"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
time.sleep(5)
# Stop ROS
print('\n')
print("2/3) Shutting down ROS...")
print('\n')
SPC.shutdown()

# Stop containers
print('\n')
print("3/3) Shutting down containers...")

bashCmd = "docker stop world drone"
process = subprocess.Popen(bashCmd.split(), stdout = subprocess.PIPE)
output, error = process.communicate()

print('\n')
print("--- DONE ---")
