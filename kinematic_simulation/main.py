"""
Simple simulation of drone flock behaviour.

Author: Nicoline Louise Thomsen
Last update: 18-02-21
"""

from ctypes import alignment
import datetime
import numpy as np
import pyautogui
import time
import tkinter as tk

from behaviour import Behaviour
from boid import Boid
import constants
from logger import Logger
from vector import Vector2D


def takeScreenshot(canvas):
    # Code from internet: https://www.javaer101.com/en/article/46892642.html
    # get the region of the canvas
    time = str(datetime.datetime.now())[11:19]
    dateid = time.replace(':', '')

    x, y = canvas.winfo_rootx(), canvas.winfo_rooty()
    w, h = canvas.winfo_width(), canvas.winfo_height()
    pyautogui.screenshot('screenshots/screenshot' + dateid +'.png', region=(x, y, w, h))


class BoardBlack(tk.Canvas):

    def __init__(self):
        super().__init__(width=constants.BOARD_SIZE, height=constants.BOARD_SIZE,
            background=constants.COLOUR_CANVAS, highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height

        self.pack(side = tk.LEFT)

        # DRAW OBSTACLES

        # Circular obstacles x, y, r
        self.obstacleList_circle = [[150, 200, 50], [700, 300, 100], [300, 500, 100]]
        # self.obstacleList_circle = [[200, 200, 20], [300, 200, 20], [400, 200, 20],
        #                     [250, 300, 20], [350, 300, 20], [450, 300, 20],
        #                     [200, 400, 20], [300, 400, 20], [400, 400, 20]]
        
        # Case d)
        self.obstacleList_circle = [[-1435, constants.BOARD_SIZE/2, 1500], [constants.BOARD_SIZE + 1435, constants.BOARD_SIZE/2, 1500], 
                            [200, 200, 50], [300, 300, 40], [500, 250, 50], [360, 500, 75], [550, 450, 30], [280, 440, 30], [175, 500, 30], [700, 400, 70]]
        
        
        # self.obstacleList_circle = []
        # self.obstacleList_box = [[400, 400, 50, 100]]
        self.obstacleList_box = []
        
        for x, y, r in self.obstacleList_circle:
            self.drawObstacles_circle(x, y, r, constants.COLOUR_OBSTACLE) 
        
        self.drawObstacles_box()

        # DRAW TARGET
        self.target = [constants.BOARD_SIZE/2, constants.BOARD_SIZE - 100]
        self.drawObstacles_circle(*self.target, 10, constants.COLOUR_GOAL)

    def drawObstacles_circle(self, x, y, r, colour):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r       
        
        self.create_oval(x0, y0, x1, y1, fill = colour, outline = "")

    def drawObstacles_box(self):

        for x, y, w, h in self.obstacleList_box:
            x0 = x - w/2
            y0 = y - h/2
            x1 = x + w/2
            y1 = y + h/2       
        
            self.create_rectangle(x0, y0, x1, y1, fill = constants.COLOUR_OBSTACLE, outline = "")


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
# flock = [Boid(boidFrame.board, *np.random.rand(2) * constants.BOARD_SIZE) for _ in range(constants.FLOCK_SIZE)]

# Case d)
start_y = 50
middle_x = constants.BOARD_SIZE/2
flock = [Boid(boidFrame.board, middle_x-20, start_y), Boid(boidFrame.board, middle_x+20, start_y), 
        Boid(boidFrame.board, middle_x-20, start_y+40), Boid(boidFrame.board, middle_x+20, start_y+40), 
        Boid(boidFrame.board, middle_x, start_y+20)]

steer = Behaviour()   # Steering vector

frame = -1
number_of_rules = 2
rule_picker = 0
slider_values = np.zeros(3)

# Logging information
log = Logger()
size_of_flock = len(flock)
cmd_collisions = 0


while True:
    frame += 1

    # Take screenshots every 50 frames, starting from frame 20 (to load gui)
    if (frame % 50 + 20) == 20:
        takeScreenshot(boidFrame.board)
    
    # # Cursor position
    # cursor_pos = [root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty()]
    # # target = cursor_pos
    
    target = boidFrame.board.target
    dist_to_target = 0

    rule_picker = (rule_picker + 1) % number_of_rules

    dst_log = []
    
    # Boid control
    for i, boid in enumerate(flock):


        # slider_values[0] = optFrame.board.alignment.get() * optFrame.board.sldr_alignment.get()      # Alignment
        # slider_values[1] = optFrame.board.cohesion.get() * optFrame.board.sldr_cohesion.get()        # Cohesion
        # slider_values[2] = optFrame.board.seperation.get() * optFrame.board.sldr_seperation.get()    # Seperation

        steer.update(boid, flock, target, rule_picker)  # Steering vector

        if steer.force.__abs__() > constants.MAX_FORCE:
            steer.force = (steer.force / steer.force.__abs__()) * constants.MAX_FORCE

        boid.update(steer.force)

        # Distance to egde of goalzone (0 while inside)
        dist_to_target += max((boid.position - Vector2D(*target)).__abs__() - constants.GOALZONE, 0)



    #     if len(dst_log) < i + 1:
    #         dst_log.append(dist_to_target)
    #     else: dst_log[i] = dist_to_target

    # log.log_to_file(frame, dst_log)

    # LOGGING
    if size_of_flock != len(flock):
        cmd_collisions += size_of_flock - len(flock)
        size_of_flock = len(flock)

    if len(flock) > 0:
        avg_dist_to_target = dist_to_target / len(flock)
        log.log_to_file(frame, avg_dist_to_target, cmd_collisions)



    # Write to labes
    # optFrame.board.text.set(str(int(Vector2D.__abs__(flock[0].velocity))))

    root.update_idletasks()
    root.update()
    time.sleep(0.01)


