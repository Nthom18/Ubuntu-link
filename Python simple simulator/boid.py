"""
Creation and management of boids on the board.

Author: Nicoline Louise Thomsen

Followed tutorial: https://medium.com/better-programming/boids-simulating-birds-flock-behavior-in-python-9fff99375118
"""
import numpy as np
import tkinter as tk
from vector import Vector2D

import constants

DOT_SIZE = 5

class Boid():

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.hitbox = DOT_SIZE
        self.colour = constants.COLOUR_WHITE

        self.perception = constants.PERCEPTION
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(*(np.random.rand(2) - 0.5) * constants.MAX_SPEED)
        self.acceleration = Vector2D(*np.zeros(2))
        # self.angle = np.degrees(np.arctan2(self.position.y,self.position.x)) # Something is wrong here

        self.dot = self.makeDot(init = True)

    def update(self, force):

        self.acceleration += force
        self.velocity += self.acceleration
        self.position += self.velocity
        

        vel = [self.velocity.x, self.velocity.y]
        if np.linalg.norm(vel) > constants.MAX_SPEED:
            self.velocity = self.velocity / np.linalg.norm(vel) * constants.MAX_SPEED

        self.outOfBounds()
        self.canvas.move(self.dot, self.velocity.x, self.velocity.y)

        self.acceleration = Vector2D(*np.zeros(2))

    def makeDot(self, init):
        if not init:
            self.canvas.delete(self.dot)

        x0 = self.position.x - DOT_SIZE
        y0 = self.position.y - DOT_SIZE
        x1 = self.position.x + DOT_SIZE
        y1 = self.position.y + DOT_SIZE
        return self.canvas.create_oval(x0, y0, x1, y1, fill = self.colour, outline = "")

    def outOfBounds(self):
        if self.position.x > constants.BOARD_SIZE:
            self.position.x = 0
            self.dot = self.makeDot(init = False)

        elif self.position.x < 0:
            self.position.x = constants.BOARD_SIZE
            self.dot = self.makeDot(init = False)

        if self.position.y > constants.BOARD_SIZE:
            self.position.y = 0
            self.dot = self.makeDot(init = False)

        elif self.position.y < 0:
            self.position.y = constants.BOARD_SIZE
            self.dot = self.makeDot(init = False)

    def lidar(self):
        a = 0

