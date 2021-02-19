"""
Simple simulation of drone flock behaviour.

Author: Nicoline Louise Thomsen
Last update: 18-02-21
"""

import numpy as np
import time
import tkinter as tk

from behaviour import Behaviour
from boid import Boid
import constants
from vector import Vector2D


class BoardBlack(tk.Canvas):

    def __init__(self):
        super().__init__(width=constants.BOARD_SIZE, height=constants.BOARD_SIZE,
            background="gray25", highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height

        self.pack(side = tk.LEFT)


class BoidFrame(tk.Frame):

    def __init__(self):
        super().__init__()

        self.master.title('Boids')
        self.board = BoardBlack()
        self.pack()


class BoardWhite(tk.Canvas):

    def __init__(self):
        super().__init__(width = constants.BOARD_SIZE/2, height = constants.BOARD_SIZE,
            background="white", highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        
        self.text = tk.StringVar()
        self.text.set("Test")
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack(fill=tk.X, padx=100)

        self.pack(side = tk.RIGHT)


class OptionFrame(tk.Frame):

    def __init__(self):
        super().__init__()

        self.board = BoardWhite()
        
        self.pack()


root = tk.Tk()
root.resizable(width = False, height = False)

boidFrame = BoidFrame()
optFrame = OptionFrame()

# Spawn boids
flock = [Boid(boidFrame.board, *np.random.rand(2) * constants.BOARD_SIZE) for _ in range(15)]


while True:
    # Boid control
    for boid in flock:

        # Calculate steering, insert steering in update
        force = Behaviour(boid).force(flock)

        boid.update(force)

    # Write to labes
    optFrame.board.text.set(str(int(Vector2D.__abs__(flock[0].velocity))))

    root.update_idletasks()
    root.update()
    time.sleep(0.01)





"""
TODO
Make restart button
"""