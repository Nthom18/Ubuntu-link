"""
Rulebase for behaviour of boids

Author: Nicoline Louise Thomsen

Followed tutorial: https://medium.com/better-programming/boids-simulating-birds-flock-behavior-in-python-9fff99375118
"""

import math
import numpy as np
from vector import Vector2D

from boid import Boid
import constants

FOV = 1/8

class Behaviour():

    def __init__(self, boid, flock, slider, rule_picker):
        self.boid = boid
        self.percieved = []

        for flockmate in flock:
            if flockmate.position.distance_to(self.boid.position) < self.boid.perception:
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
            steering = avg_vec - self.boid.velocity

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
            vec_to_com = center_of_mass - self.boid.position

            if vec_to_com.__abs__() > 0:
                vec_to_com = (vec_to_com / vec_to_com.__abs__()) * constants.MAX_SPEED
            
            steering = vec_to_com - self.boid.velocity

        return steering


    def separation(self):
        steering = Vector2D(*np.zeros(2))
        avg_vector = Vector2D(*np.zeros(2))
        total = 0
        for flockmate in self.percieved:
            distance = flockmate.position.distance_to(self.boid.position)
            
            if self.boid.position != flockmate.position and distance < (self.boid.perception / 3):
                diff = self.boid.position - flockmate.position

                avg_vector += diff
                total += 1

        if total > 0:
            avg_vector /= total

            if steering.__abs__() > 0:
                avg_vector = (avg_vector / steering.__abs__()) * constants.MAX_SPEED
            
            if avg_vector.__abs__() > 0:
                steering = avg_vector - self.boid.velocity

        return steering


    def obstacle_avoidance(self):
        object_detected = False
        min_ray = Vector2D(*np.zeros(2))

        left = self.boid.lidar[- math.ceil(len(self.boid.lidar) * FOV/2) :]
        right = self.boid.lidar[: math.ceil(len(self.boid.lidar) * FOV/2)]
        fov = left + right

        print(fov)

        # for ray in fov:
            

        #     min_ray = min(min_ray, ray)
        #     if ray < self.boid.perception:
        #         object_detected = True
    
        if object_detected:
            return min_ray - self.boid.velocity

        return Vector2D(*np.zeros(2))