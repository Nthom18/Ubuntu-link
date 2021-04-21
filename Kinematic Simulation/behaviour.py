"""
Rulebase for behaviour of drones

Author: Nicoline Louise Thomsen

Followed tutorial for boids behaviour: https://medium.com/better-programming/drones-simulating-birds-flock-behavior-in-python-9fff99375118
"""

import math
import numpy as np
import pyautogui
from vector import Vector2D

from boid import Boid
import constants

FOV = 1/4
MARGIN = 20

class Behaviour():

    def __init__(self):
        self.drone = []
        self.percieved_flockmates = []
        self.force = 0

    def update(self, drone, flock, target, slider, rule_picker):
        self.drone = drone
        self.percieved_flockmates.clear()
        for flockmate in flock:
            if flockmate.position.distance_to(self.drone.position) < self.drone.perception:
                self.percieved_flockmates.append(flockmate)

        switcher = {
            0: slider[0] * self.alignment(),
            1: slider[1] * self.cohesion(),
            2: slider[2] * self.separation()
        }
        
        # Priority rule selection
        if self.obstacle_avoidance().__abs__() > 0: self.force = self.obstacle_avoidance()
        else: self.force = switcher.get(rule_picker) + self.seek(target)



    def alignment(self):
        steering = Vector2D(*np.zeros(2))
        avg_vec = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in self.percieved_flockmates:
            avg_vec += flockmate.velocity
            total += 1
        
        if total > 0:
            avg_vec /= total
            avg_vec = (avg_vec / avg_vec.__abs__()) * constants.MAX_SPEED
            steering = avg_vec - self.drone.velocity

        return steering


    def cohesion(self):
        steering = Vector2D(*np.zeros(2))
        center_of_mass = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in self.percieved_flockmates:
            center_of_mass += flockmate.position
            total += 1

        if total > 0:
            center_of_mass /= total
            vec_to_com = center_of_mass - self.drone.position

            if vec_to_com.__abs__() > 0:
                vec_to_com = (vec_to_com / vec_to_com.__abs__()) * constants.MAX_SPEED
            
            steering = vec_to_com - self.drone.velocity

        return steering


    def separation(self):
        steering = Vector2D(*np.zeros(2))
        avg_vector = Vector2D(*np.zeros(2))
        total = 0
        for flockmate in self.percieved_flockmates:
            distance = flockmate.position.distance_to(self.drone.position)
            
            if self.drone.position != flockmate.position and distance < (self.drone.perception / 3):
                diff = self.drone.position - flockmate.position

                avg_vector += diff
                total += 1

        if total > 0:
            avg_vector /= total

            if steering.__abs__() > 0:
                avg_vector = (avg_vector / steering.__abs__()) * constants.MAX_SPEED
            
            if avg_vector.__abs__() > 0:
                steering = avg_vector - self.drone.velocity

        return steering


    def obstacle_avoidance(self):
        steering = Vector2D(*np.zeros(2))
        max_ray = 0
        max_ray_index = 0
        object_detected = False

        if len(self.drone.lidar.sensorReadings) != 0:
            step_angle = 360 / len(self.drone.lidar.sensorReadings)

        fov = math.ceil(len(self.drone.lidar.sensorReadings) * FOV/2)
        
        left = self.drone.lidar.sensorReadings[-fov:]
        right = self.drone.lidar.sensorReadings[:fov]


        # Check rays
        for i, ray in enumerate(left):
            if ray < self.drone.perception - MARGIN:
                object_detected = True
            
            if max_ray < ray:
                max_ray = ray
                max_ray_index = i
        
        right.reverse()
        for i, ray in enumerate(right):
            if ray < self.drone.perception - MARGIN:
                object_detected = True
            
            if max_ray < ray:
                max_ray = ray
                max_ray_index = 2 * len(right) - 1 - i  # Offset and reverse indexing
    
        if object_detected:
            # Give ray reading a direction
            dir = self.drone.velocity.rotate(math.radians((max_ray_index - fov) * step_angle))
            steering = dir.norm() - self.drone.velocity.norm()
            return steering.norm() * constants.MAX_FORCE 

        return steering

    def seek(self, target):
        steering = Vector2D(*np.zeros(2))
        dir = Vector2D(*np.zeros(2))

        dir = Vector2D(*target) - self.drone.position
        
        steering = dir.norm() - self.drone.velocity.norm()
        return steering.norm() * constants.MAX_FORCE 

