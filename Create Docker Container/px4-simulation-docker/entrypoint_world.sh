#!/bin/bash
set -e

# setup ros environment
source /root/catkin_ws/devel/setup.bash

export ROS_IP=$(hostname -I | awk '{print $1;}')
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI=http://$ROS_HOSTNAME:$2

source /root/setup_gazebo.bash

# ensure inputs are correct
if [ "$#" -eq 3 ]; then
    echo "Gazebo master port will be $1"
    echo "Roscore port: $2"
    echo "World: $3"
else
    echo "Invalid parameters: [<port for gazebo master> <port for ros master> <environment>]"
    exit 1;
fi

#sed -i 's/127.0.0.1/'$3'/g' ${FIRMWARE_DIR}/Tools/sitl_gazebo/models/sdu_mono_cam/model.sdf

# set gazebo port
export GAZEBO_MASTER_URI=http://localhost:$1

#roscore -p $2 &

echo "ROS_IP: $ROS_IP"
echo "ROS_HOSTNAME: $ROS_HOSTNAME"
echo "ROS_MASTER_URI: $ROS_MASTER_URI"

# Fix /camera display issue: https://answers.gazebosim.org//question/14625/running-a-camera-sensor-headless/
Xvfb :1 -screen 0 1600x1200x16  &
export DISPLAY=:1.0

#source ${WORKSPACE_DIR}/edit_rcS.bash $1 &&
#roslaunch px4 vm_docker_posix_sitl.launch gui:=false tcp_port:=$3 udp_port:=$4
#HEADLESS=1 make px4_sitl_default gazebo_$3

roslaunch eit_playground posix_world.launch env:=$3
