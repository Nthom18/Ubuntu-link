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

    def force(self, flock):
        alignment = self.alignment(flock)
        cohesion = self.cohesion(flock)
        separation = self.separation(flock)
        return alignment * ALIGN_FACTOR + cohesion * COHESION_FACTOR + separation * SEPERTION_FACTOR

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

        return steering

    def cohesion(self, flock):
        # steering = Vector2D(*np.zeros(2))
        center_of_mass = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in flock:
            diff = [flockmate.position.x - self.boid.position.x, flockmate.position.y - self.boid.position.y]
            if np.linalg.norm(diff) < self.boid.perception:
                center_of_mass += flockmate.position
                total += 1

        if total > 0:
            center_of_mass /= total
            vec_to_com = [center_of_mass.x - self.boid.position.x, center_of_mass.y - self.boid.position.y]
            
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * constants.MAX_SPEED
            
            steering = [vec_to_com[0] - self.boid.velocity.x, vec_to_com[1] - self.boid.velocity.y]
            
            if np.linalg.norm(steering) > constants.MAX_FORCE:
                steering = (steering /np.linalg.norm(steering)) * constants.MAX_FORCE

        return Vector2D(steering[0], steering[1])

    def separation(self, flock):
        # steering = Vector2D(*np.zeros(2))
        steering = [0, 0]
        avg_vector = Vector2D(*np.zeros(2))
        total = 0
        for flockmate in flock:
            diff = [flockmate.position.x - self.boid.position.x, flockmate.position.y - self.boid.position.y]
            distance = np.linalg.norm(diff)
            if self.boid.position != flockmate.position and distance < self.boid.perception:
                diff = self.boid.position - flockmate.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * constants.MAX_SPEED
            steering = [avg_vector.x - self.boid.velocity.x, avg_vector.y - self.boid.velocity.y]
            if np.linalg.norm(steering) > constants.MAX_FORCE:
                steering = (steering /np.linalg.norm(steering)) * constants.MAX_FORCE

        return Vector2D(steering[0], steering[1])

    
