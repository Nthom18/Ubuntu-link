#!/bin/bash

gcc -Wall -o Light light.c -lwiringPi
./Light &

