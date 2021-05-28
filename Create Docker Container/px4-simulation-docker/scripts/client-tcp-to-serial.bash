#!/bin/bash
# Script for connecting Mavlink TCP instance from our headless docker image on our VM to the local computer. 
# 
# Script created by Frederik Mazur Andersen <fm@mmmi.sdu.dk> 

usage="
$(basename "$0") [-h] [TCP PORT]
 
A script to setup communication translation from VM TCP port to local serial device

TCP_PORT the port of simulation servers Mavlink instance for simulation
"

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "$usage" >&2
    exit 1
fi

echo "Starting virtuel serial ports: /tmp/PX1 and /tmp/PX2"
socat -d -d pty,raw,echo=0,link=/tmp/PX1 pty,raw,echo=0,link=/tmp/PX2 &

echo "Starting socat reading from fun-fred on port $1 and linking to /tmp/PX1"
socat -d PTY,link=/tmp/PX1 tcp:fun-fred.sandbox.tek.sdu.dk:$1