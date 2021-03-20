"""
Simple simulation of drone flock behaviour.

Author: Nicoline Louise Thomsen
Last update: 18-02-21
"""

from ctypes import alignment
import numpy as np
import time
import tkinter as tk

from behaviour import Behaviour
from boid import Boid
import constants
from vector import Vector2D

FLOCK_SIZE = 30


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
            highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        
        # Test Label
        # self.text = tk.StringVar()
        # self.label = tk.Label(self, textvariable=self.text)
        # self.label.pack(fill=tk.X, padx = 100)

        # Alignment options
        self.alignment = tk.IntVar(value = 1)
        self.chk_alignment = tk.Checkbutton(self, text = 'Alignment', variable = self.alignment)
        self.chk_alignment.pack()

        self.sldr_alignment = tk.Scale(self, from_ = 0, to = 20, tickinterval = 1, length = constants.BOARD_SIZE/2 - 80, digits = 2, orient = tk.HORIZONTAL)
        self.sldr_alignment.pack()

        # Cohesion options
        self.cohesion = tk.IntVar(value = 1)
        self.chk_cohesion = tk.Checkbutton(self, text = 'Cohesion', variable = self.cohesion)
        self.chk_cohesion.pack()

        self.sldr_cohesion = tk.Scale(self, from_ = 0, to = 20, tickinterval = 1, length = constants.BOARD_SIZE/2 - 80, digits = 2, orient = tk.HORIZONTAL)
        self.sldr_cohesion.pack()

        # Seperation options
        self.seperation = tk.IntVar(value = 1)
        self.chk_seperation = tk.Checkbutton(self, text = 'Seperation', variable = self.seperation)
        self.chk_seperation.pack()

        self.sldr_seperation = tk.Scale(self, from_ = 0, to = 20, tickinterval = 1, length = constants.BOARD_SIZE/2 - 80, digits = 2, orient = tk.HORIZONTAL)
        self.sldr_seperation.pack()



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
flock = [Boid(boidFrame.board, *np.random.rand(2) * constants.BOARD_SIZE) for _ in range(FLOCK_SIZE)]



while True:
    # Boid control
    for boid in flock:

        # Using sliders to weigh values
        a = optFrame.board.alignment.get() * optFrame.board.sldr_alignment.get()
        c = optFrame.board.cohesion.get() * optFrame.board.sldr_cohesion.get()
        s = optFrame.board.seperation.get() * optFrame.board.sldr_seperation.get()

        force = Behaviour(boid, flock, a, c, s).force

        if force.__abs__() > constants.MAX_FORCE:
            force = (force / force.__abs__()) * constants.MAX_FORCE

        boid.update(force)

    # Write to labes
    # optFrame.board.text.set(str(int(Vector2D.__abs__(flock[0].velocity))))

    root.update_idletasks()
    root.update()
    time.sleep(0.01)





"""
TODO
Make restart button
"""