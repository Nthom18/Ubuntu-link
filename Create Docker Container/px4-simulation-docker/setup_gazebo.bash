#!/bin/bash
#source "/opt/ros/melodic/setup.bash"

source /root/Firmware/Tools/setup_gazebo.bash /root/Firmware/ /root/Firmware/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/Firmware
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:/root/Firmware/Tools/sitl_gazebo

echo ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH
