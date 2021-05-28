#!/bin/bash
set -e

# setup ros environment

echo ">> Creating catkin workspace"
source "/opt/ros/melodic/setup.bash"

catkin_init_workspace

echo ">> Build the catkin workspace"
cd ../ && catkin build
