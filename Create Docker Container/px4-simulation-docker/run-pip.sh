#!/bin/bash
set -e

# setup ros environment

pip install -r /root/catkin_ws/src/requirements.txt
pip3 install -r /root/catkin_ws/src/requirements.txt

pip install catkin_tools wstool --upgrade
pip3 install Pillow
