'''
Translator between offb_posctl.py and behaviour.py.

Author: Nicoline Louise Thomsen
'''

import numpy as np

import offb_posctl as offb

from kinematic_simulation_copy.vector import Vector2D

from kinematic_simulation_copy.lidar import LiDAR

class Drone():

    def __init__(self, drone_controller, id):

        self.id = id
        offset = id

        self.max_speed = 10
        self.hitbox = 1
        self.perception = 4

        self.me = drone_controller

        self.position = Vector2D(drone_controller.target.pose.position.x, 
                                 drone_controller.target.pose.position.y + offset)
        
        self.velocity = Vector2D(*(np.random.rand(2) - 0.5) * 0.01)
        # self.velocity = Vector2D(*np.zeros(2))
        
        self.acceleration = Vector2D(*np.zeros(2))

        self.collision_flag = False

        # LiDAR
        self.obstacleList_circle = [[5.9, -22.5, 1.5], [-12.85, -25, 1.5], [-7.6, -22, 1.5], [6.6, -15, 2], [11.6, -10, 2.5], [3.4, -12.5, 2.5], [13.4, -20, 3.5], [-3.6, -25, 3.75], [-93.35, -21.6, 75], [93.35, -21.6, 75]]
        self.lidar = LiDAR(self, self.obstacleList_circle)


    def update(self, force):

        self.acceleration += force
        self.velocity += self.acceleration
        self.position += self.velocity

        self.me.target.pose.position.x = self.position.x
        self.me.target.pose.position.y = self.position.y
        
        self.acceleration = Vector2D(*np.zeros(2))

        # print(self.id, ": ", self.position)



