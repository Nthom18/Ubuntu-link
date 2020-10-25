#!/bin/bash

# Ctrl-C handler
#shutdown()
#{
#  echo hello
#  exit 0
#}

#trap shutdown EXIT

# Compile and run in background
gcc -Wall -o Light light.c -lwiringPi
./Light

