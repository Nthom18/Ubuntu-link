'''
Rulebase for behaviour of drones

Author: Nicoline Louise Thomsen

Inspiration from tutorial for boids behaviour: 
https://medium.com/better-programming/drones-simulating-birds-flock-behavior-in-python-9fff99375118
The code have been changed to use the datastructure of the Vector2D class, changed the gui package, and other modifications to improve the behaviour for use on drone platforms.
'''

import math
import numpy as np
from vector import Vector2D

from boid import Boid
import constants

FOV = 1/6
MARGIN = 20
STOP_FORCE = 0.5
MAX_DRONE_PR_TREE = 3
TIME_TO_ANALYZE = 1000

class Behaviour():

    def __init__(self, case_id, obstacle_list):
        self.drone = []
        self.percieved_flockmates = []
        self.force = 0
        self.case_id = case_id
        
        # Case c) specific
        self.trees = obstacle_list[2:]
        self.analyzed_trees = np.zeros(len(self.trees))     # Binary checklist
        self.analyzing_trees = np.zeros(len(self.trees))    # Array denoting number of drones on a tree
        self.tree_timers = np.zeros(len(self.trees)) + TIME_TO_ANALYZE

        self.break_flag = False


    def update(self, drone, flock, target, rule_picker):
        self.drone = drone
        self.percieved_flockmates.clear()
        for flockmate in flock:
            if 0 < flockmate.position.distance_to(self.drone.position) < self.drone.perception:
                if flockmate.collision_flag == False:
                    self.percieved_flockmates.append(flockmate)

        switcher = {
            0: self.alignment(),
            1: self.cohesion()
        }
        
        # Priority rule selection
        if self.obstacle_avoidance().__abs__() > 0 or self.separation().__abs__() > 0: 
            self.force = self.obstacle_avoidance() + self.separation()

        # Case c)
        elif self.case_id == 'c':
            self.case_c(target)
            
        # Case d)
        elif self.case_id == 'd':
            self.case_d(target, switcher.get(rule_picker))
            
        # Aimless flight
        else: self.force = switcher.get(rule_picker)


############################# CASES #############################

    def case_c(self, target):
        # Choose tree to analyze
        for tree_id in range(len(self.trees)):
            
            # Tree analyze timer
            if self.tree_timers[tree_id] > 0:
                self.tree_timers[tree_id] -= self.analyzing_trees[tree_id]
            elif self.analyzed_trees[tree_id] == False:
                self.analyzed_trees[tree_id] = True
                self.analyzing_trees[tree_id] = 0 # For debug info
            else:
                self.drone.analyzing_in_progress[tree_id] = False

            # If not already analyzing
            if not any(self.drone.analyzing_in_progress):
                # Start analyze tree if unanalyzed and not full
                if self.analyzed_trees[tree_id] == False:
                    if self.analyzing_trees[tree_id] < MAX_DRONE_PR_TREE:
                        self.drone.target_tree = [self.trees[tree_id][0], self.trees[tree_id][1]]
                        # Only be part of analyzing group if close enough
                        if self.drone.position.distance_to(Vector2D(*self.drone.target_tree)) < 50:
                            self.analyzing_trees[tree_id] += 1
                            self.drone.analyzing_in_progress[tree_id] = True

        if all(self.analyzed_trees):
            self.break_flag = True

        else:
            self.force = self.seek(self.drone.target_tree)


    def case_d(self, target, boid_force):
        # Stop when goalsonze is reached
        if self.drone.position.distance_to(Vector2D(*target)) < constants.GOALZONE:
            if self.drone.velocity.__abs__() != 0:
                self.force = - self.drone.velocity * STOP_FORCE
            else:
                self.force = Vector2D(*np.zeros(2)) 
        # Only focus on seek if goalzone is near
        elif self.drone.position.distance_to(Vector2D(*target)) < constants.GOALZONE * 2:
            self.force = self.seek(target)
        # Normal operation if goalzone is far
        else: self.force = boid_force + self.seek(target)


############################# BEHAVIOURS #############################

    def alignment(self):
        steering = Vector2D(*np.zeros(2))
        avg_vec = Vector2D(*np.zeros(2))
        total = 0

        for flockmate in self.percieved_flockmates:
            avg_vec += flockmate.velocity
            total += 1
        
        if total > 0:
            avg_vec /= total
            steering = avg_vec - self.drone.velocity

        if steering.__abs__() > constants.MAX_FORCE:
            steering = steering.norm() * constants.MAX_FORCE

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
            steering = vec_to_com - self.drone.velocity

        if steering.__abs__() > constants.MAX_FORCE:
            steering = steering.norm() * constants.MAX_FORCE

        return steering


    def separation(self):
        steering = Vector2D(*np.zeros(2))
        avg_vector = Vector2D(*np.zeros(2))
        total = 0
        
        for flockmate in self.percieved_flockmates:
            distance = flockmate.position.distance_to(self.drone.position)
            
            if distance < (self.drone.perception / 4):
                diff = self.drone.position - flockmate.position

                avg_vector += diff
                total += 1

            # COLLISION CHECK
            if distance < constants.DRONE_RADIUS:
                self.drone.collision_flag = True
                flockmate.collision_flag = True

        if total > 0:
            avg_vector /= total
            
            if avg_vector.__abs__() > 0:
                steering = avg_vector - self.drone.velocity

        return steering.norm() * constants.MAX_FORCE


    def obstacle_avoidance(self):
        step_angle = 0
        if len(self.drone.lidar.sensorReadings) != 0:
            step_angle = 360 / len(self.drone.lidar.sensorReadings)

        near = self.drone.perception - MARGIN
        too_close = 4 * constants.DRONE_RADIUS


        return self.avoid(too_close, step_angle) + self.evade(too_close, near, step_angle, )

    # Flies directly in the oposite direction of close objects
    def avoid(self, too_close, step_angle):
        steering = Vector2D(*np.zeros(2))
        avg_vec = Vector2D(*np.zeros(2))
        total = 0

        for index, ray in enumerate(self.drone.lidar.sensorReadings):
            # if the drone is too close to object (four times its own radius from its centerpoint)
            if ray < too_close:
                avg_vec += self.drone.velocity.rotate(math.radians(index * step_angle))
                total += 1
            
            # COLLISION CHECK (a drone can only hit an object if moving)
            if ray < constants.DRONE_RADIUS and self.drone.velocity.__abs__() > 0:
                self.drone.collision_flag = True

        if avg_vec.__abs__() != 0:
            avg_vec /= total
            avg_vec = avg_vec.norm() * constants.MAX_SPEED

        if total > 0:
            # Fly away!
            steering = -avg_vec - self.drone.velocity
            return steering.norm() * constants.MAX_FORCE 
        
        return steering

    # Flying around upcomming obstacles
    def evade(self, too_close, near, step_angle):
        steering = Vector2D(*np.zeros(2))
        max_ray = 0
        max_ray_index = 0
        front_object_detected = False

        fov = math.ceil(len(self.drone.lidar.sensorReadings) * FOV/2)

        left = self.drone.lidar.sensorReadings[-fov:]
        right = self.drone.lidar.sensorReadings[:fov]


        # Check rays, they have to be within range and not too close to be evaded
        for i, ray in enumerate(left):
            if too_close < ray < near:
                front_object_detected = True
            
            if max_ray < ray:
                max_ray = ray
                max_ray_index = i
        
        right.reverse()
        for i, ray in enumerate(right):
            if too_close < ray < near:
                front_object_detected = True
            
            if max_ray < ray:
                max_ray = ray
                max_ray_index = 2 * len(right) - 1 - i  # Offset and reverse indexing
    
        if front_object_detected:
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


