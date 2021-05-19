import numpy as np

import offb_posctl as offb

from kinematic_simulation_copy.vector import Vector2D

class Drone():

    def __init__(self, drone_controller, id):
        self.max_speed = 10

        self.hitbox = 1
        self.perception = 5
        
        offset = id

        self.position = Vector2D(drone_controller.target.pose.position.x, drone_controller.target.pose.position.y + offset)
        self.velocity = Vector2D(*(np.random.rand(2) - 0.5) * self.max_speed)
        self.acceleration = Vector2D(*np.zeros(2))

        self.collision_flag = False

        # self.lidar = LiDAR(self, self.canvas.obstacleList_circle, self.canvas.obstacleList_box, self.canvas)

        print(self.position)





    def update(self, force):

        self.acceleration += force
        self.velocity += self.acceleration
        self.position += self.velocity
        

        vel = [self.velocity.x, self.velocity.y]
        if np.linalg.norm(vel) > self.velocity:
            self.velocity = self.velocity / np.linalg.norm(vel) * self.max_speed

        self.acceleration = Vector2D(*np.zeros(2))

        # self.lidar.update(self)s


