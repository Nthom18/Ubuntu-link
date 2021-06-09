'''
Translator between offb_posctl.py and behaviour.py.

Author: Nicoline Louise Thomsen
'''

import numpy as np

import offb_posctl as offb

from kinematic_simulation_copy.vector import Vector2D

import kinematic_simulation_copy.constants as constants
from kinematic_simulation_copy.lidar import LiDAR


class Drone():

    def __init__(self, drone_controller, id):

        self.id = id
        offset = id

        self.max_speed = constants.MAX_SPEED
        self.hitbox = constants.DRONE_RADIUS
        self.perception = constants.PERCEPTION

        self.me = drone_controller

        self.position = Vector2D(drone_controller.target.pose.position.x, 
                                 drone_controller.target.pose.position.y + offset)
        
        # self.velocity = Vector2D(*(np.random.rand(2) - 0.5) * 0.01)
        self.velocity = Vector2D(*np.zeros(2))
        
        self.acceleration = Vector2D(*np.zeros(2))

        self.collision_flag = False

        # LiDAR
        self.lidar = LiDAR(self, constants.OBSTACLE_LIST)


    def update(self, force):

        self.acceleration += force
        self.velocity += self.acceleration
        self.position += self.velocity

        self.me.target.pose.position.x = self.position.x
        self.me.target.pose.position.y = self.position.y
        
        self.acceleration = Vector2D(*np.zeros(2))

        # print(self.id, ": ", self.position)



