'''
Using the principle of Ray Marching 
from Sebastion Lague Youtube video:

https://www.youtube.com/watch?v=Cp5WWtMoeKg&ab_channel=SebastianLague
'''

import numpy as np
from vector import Vector2D

import constants

class LIDAR():

    def __init__(self, boidPos, obstacleList, canvas):
        self.point = boidPos
        self.obstacles = obstacleList
        self.sensorReadings = []

        # Debug visualization
        self.canvas = canvas
        self.distanceCircle = self.canvas.create_oval(0, 0, 100, 100, fill = constants.COLOUR_GREY, outline = "")

    def signedDistToScene(self):
        distToScene = constants.BOARD_SIZE

        for circle in self.obstacles:
            distToCircle = self.signedDistToCircle(circle)
            distToScene = min(distToCircle, distToScene)
        
        print(distToScene)

        # self.canvas.delete(self.distanceCircle)
        self.drawDistance(distToScene)
        
        return distToScene

    def signedDistToCircle(self, circle):
        centre = Vector2D(circle[0], circle[1])
        radius = circle[2]
        return self.length(centre - self.point) - radius

    def length(self, v):
        return np.sqrt(v.x**2 + v.y**2)

    def drawDistance(self, distance):
        x0 = self.point.x - distance
        y0 = self.point.y - distance
        x1 = self.point.x + distance
        y1 = self.point.y + distance

        self.canvas.coords(self.distanceCircle, x0, y0, x1, y1)
