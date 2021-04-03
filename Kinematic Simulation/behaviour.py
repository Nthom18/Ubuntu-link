"""
Rulebase for behaviour of drones

Author: Nicoline Louise Thomsen

Followed tutorial for boids behaviour: https://medium.com/better-programming/drones-simulating-birds-flock-behavior-in-python-9fff99375118
"""

import math
import numpy as np
from vector import Vector2D

from boid import Boid
import constants

FOV = 1/8
MARGIN = 20

class Behaviour():

    def __init__(self, drone):
        self.drone = drone
        self.percieved = []
        self.force = 0

    def update(self, drone, flock, slider, rule_picker):
        self.drone = drone
        self.percieved.clear()
        for flockmate in flock:
            if flockmate.position.distance_to(self.drone.position) < self.drone.perception:
                self.percieved.append(flockmate)

        switcher = {
            0: slider * self.alignment(),
            1: slider * self.cohesion(),
            2: slider * self.separation(),
            3: self.obstacle_avoidance()
        }

        self.force = switcher.get(rule_picker)

    def alignment(self):
        steering = Vector2D(*np.zeros(2))
        avg_vec = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in self.percieved:
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

        for flockmate in self.percieved:
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
        for flockmate in self.percieved:
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
        vision = left + right

        for i, ray in enumerate(vision):
            if ray < self.drone.perception - MARGIN:
                object_detected = True
            
            if max_ray < ray:
                max_ray = ray
                max_ray_index = i
    
        if object_detected:
            # Give ray reading a direction
            dir = self.drone.velocity.rotate(math.radians((max_ray_index - fov) * step_angle))
            steering = dir.norm() * constants.MAX_FORCE - self.drone.velocity
            return steering 

        return steering