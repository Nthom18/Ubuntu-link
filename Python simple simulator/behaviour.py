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

ALIGN_FACTOR = 0.01
COHESION_FACTOR = 0
SEPERTION_FACTOR = 0

class Behaviour():

    def __init__(self, boid):
        self.boid = boid

    def alignment(self, flock):
        steering = Vector2D(*np.zeros(2))
        avg_vec = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in flock:
            diff = [flockmate.position.x - self.boid.position.x, flockmate.position.y - self.boid.position.y]
            if np.linalg.norm(diff) < self.boid.perception:
                avg_vec += flockmate.velocity
                total += 1
        
        if total > 0:
            avg_vec /= total
            avg_vec = (avg_vec /np.linalg.norm([avg_vec.x, avg_vec.y])) * constants.MAX_SPEED
            steering = avg_vec - self.boid.velocity

        # if steering.__abs__() > constants.MAX_FORCE:
        #     steering = (steering / steering.__abs__()) * constants.MAX_FORCE

        return steering

    def cohesion(self, flock):
        center_of_mass = Vector2D(*np.zeros(2))
        steering = [0,0]
        total = 0

        for flockmate in flock:
            if flockmate.position.distance_to(self.boid.position) < self.boid.perception:
                center_of_mass += flockmate.position
                total += 1

        if total > 0:
            center_of_mass /= total
            vec_to_com = [center_of_mass.x - self.boid.position.x, center_of_mass.y - self.boid.position.y]
            
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * constants.MAX_SPEED
            
            steering = [vec_to_com[0] - self.boid.velocity.x, vec_to_com[1] - self.boid.velocity.y]

        return Vector2D(steering[0], steering[1])

    def separation(self, flock):
        steering = Vector2D(*np.zeros(2))
        avg_vector = Vector2D(*np.zeros(2))
        total = 0
        for flockmate in flock:
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


