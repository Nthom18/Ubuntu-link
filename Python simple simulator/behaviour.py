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

class Behaviour():

    def __init__(self, boid, flock, a, c, s):
        self.boid = boid
        self.percieved = []

        for flockmate in flock:
            if flockmate.position.distance_to(self.boid.position) < self.boid.perception:
                self.percieved.append(flockmate)

        self.force = a * self.alignment() + c * self.cohesion() + s * self.separation()


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


