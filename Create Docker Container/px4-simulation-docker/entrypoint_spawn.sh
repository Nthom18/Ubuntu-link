#!/bin/bash
set -e

# setup ros environment
source /root/catkin_ws/devel/setup.bash

export ROS_IP=$(hostname -I | awk '{print $1;}')
export ROS_HOSTNAME=$ROS_IP
export ROS_MASTER_URI=http://$ROS_HOSTNAME:$3

source /root/setup_gazebo.bash

# ensure inputs are correct
if [ "$#" -eq 7 ]; then
    echo "QGC udp port will be $1"
    echo "Gazebo master port will be $2"
    echo "Roscore port: $3"
    echo "Model: $4"
    echo "ID: $5"
    echo "pos x: $6"
    echo "pos y: $7"
else
    echo "Invalid parameters: [<udp port for PX4> <port for gazebo master>]"
    exit 1;
fi

#sed -i 's/127.0.0.1/'$3'/g' ${FIRMWARE_DIR}/Tools/sitl_gazebo/models/sdu_mono_cam/model.sdf

# set gazebo port
export GAZEBO_MASTER_URI=http://localhost:$2

echo "ROS_IP: $ROS_IP"
echo "ROS_HOSTNAME: $ROS_HOSTNAME"
echo "ROS_MASTER_URI: $ROS_MASTER_URI"

export MAVPROXY_UDP_PORT=$((14540+$5))
echo "MAVPROXY_UDP_PORT: $MAVPROXY_UDP_PORT"


# Fix /camera display issue: https://answers.gazebosim.org//question/14625/running-a-camera-sensor-headless/
#Xvfb :1 -screen 0 1600x1200x16  &
#export DISPLAY=:1.0

#source ${WORKSPACE_DIR}/edit_rcS.bash $1 &&
#roslaunch px4 vm_docker_posix_sitl.launch gui:=false tcp_port:=$3 udp_port:=$4
#HEADLESS=1 make px4_sitl_default gazebo_$3

roslaunch eit_playground posix_spawn.launch vehicle:=$4 ID:=$5 x:=$6 y:=$7
#&
#sleep 10
#mavproxy.py --master=udp:localhost:$MAVPROXY_UDP_PORT --out=udp:localhost:$1
