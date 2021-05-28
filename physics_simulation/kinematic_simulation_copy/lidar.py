'''
Using the principle of Ray Marching 
from Sebastion Lague Youtube video:

https://www.youtube.com/watch?v=Cp5WWtMoeKg&ab_channel=SebastianLague
'''

import math
import numpy as np
from kinematic_simulation_copy.vector import Vector2D

import kinematic_simulation_copy.constants

THRESHOLD = 0.1
MAX_MARCHING_STEPS = 15
FULL_CIRCLE = 360
RESOLUTION = 1 / 8

class LiDAR():

    def __init__(self, originPoint, obstacleList_circle):
        self.oPos = originPoint.position
        self.oDir = originPoint.velocity.norm()
        self.range = originPoint.perception
        self.obstacles_circle = obstacleList_circle
        self.sensorReadings = []



    def update(self, originPoint):
        # DEBUG visualization
        self.canvas.delete("red")
        self.canvas.delete("grey")
        # -------------------

        self.oPos = originPoint.position
        self.oDir = originPoint.velocity.norm()

        self.sensorReadings.clear()
        self.rayMarching()
        

    def rayMarching(self):
        for i in range(int(FULL_CIRCLE * RESOLUTION)):
            dot = self.sphereTracing(self.oDir.rotate(math.radians(i / RESOLUTION)))
            self.sensorReadings.append(self.oPos.distance_to(dot))


    def sphereTracing(self, dir):
        p = self.oPos
        distToScene = self.signedDistToScene(p)

        for i in range(MAX_MARCHING_STEPS):
            p = p + dir * distToScene
            distToScene = self.signedDistToScene(p)

            if distToScene < THRESHOLD:
                return p
            
            if self.oPos.distance_to(p) > self.range:
                return self.oPos + dir * self.range

        return self.oPos + dir * self.range
        

    def signedDistToScene(self, p):
        distToScene = 864/20    # kinematic board size after rescaling

        for circle in self.obstacles_circle:
            distToCircle = self.signedDistToCircle(p, circle)
            distToScene = min(distToCircle, distToScene)

        # for box in self.obstacles_box:
        #     distToBox = self.signedDistToBox(p, box)
        #     distToScene = min(distToBox, distToScene)

        # # DEBUG
        # self.drawDistance(distToScene)
        # print(distToScene)

        return distToScene


    def signedDistToCircle(self, p, circle):
        centre = Vector2D(circle[0], circle[1])
        radius = circle[2]
        return self.length(centre - p) - radius

    def signedDistToBox(self, p, box):
        centre = Vector2D(box[0], box[1])
        size = Vector2D(box[2], box[3])
        offset = ((centre - p).positive() - size).__abs__()

        # d = np.sqrt(max(centre.x - size.x/2 - p.x, 0)**2 + max(centre.y - size.y/2 - p.y, 0)**2)
        
        # dst from point outside box to edge (0 if inside box)
        unsignedDst = max(offset, 0)
        # -dst from point inside box to edge (0 if outside box)
        # dstInsideBox = max(min(offset, 0))

        return unsignedDst
        # return constants.BOARD_SIZE


    def length(self, v):
        return np.sqrt(v.x**2 + v.y**2)
