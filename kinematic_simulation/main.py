"""
Simple simulation of drone flock behaviour.

Author: Nicoline Louise Thomsen
Last update: 31-05-21
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

    def __init__(self, case_id):
        super().__init__(width=constants.BOARD_SIZE, height=constants.BOARD_SIZE,
            background=constants.COLOUR_CANVAS, highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height

        self.pack(side = tk.LEFT)

        # DRAW OBSTACLES (Circular obstacles x, y, r)
        # Borders
        self.obstacleList_box = []
        self.obstacleList_circle = [[-1435, constants.BOARD_SIZE/2, 1500], [constants.BOARD_SIZE + 1435, constants.BOARD_SIZE/2, 1500]]        

        # Case c)
        if case_id == 'c':
            self.obstacleList_circle.extend([[200, 200, 20], [500, 300, 20], [300, 500, 20], [600, 600, 20]])

        # Case d)
        elif case_id == 'd':
            self.obstacleList_circle.extend([[200, 200, 50], [300, 300, 40], [500, 250, 50], [360, 500, 75], [550, 450, 30], [280, 440, 30], [175, 500, 30], [700, 400, 70]])
        
        # Default
        else:
            self.obstacleList_circle.extend([[150, 200, 50], [700, 300, 100], [300, 500, 100]])
            # self.obstacleList_circle = [[200, 200, 20], [300, 200, 20], [400, 200, 20],
            #                 [250, 300, 20], [350, 300, 20], [450, 300, 20],
            #                 [200, 400, 20], [300, 400, 20], [400, 400, 20]]
            
        
        
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

    def __init__(self, case_id):
        super().__init__()

        self.master.title('Kinematic simulation case ' +  case_id + ')')
        self.board = BoardBlack(case_id)
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


def main(frame_duration, case_id, test_id, flock_size):

    root = tk.Tk()
    root.resizable(width = False, height = False)

    boidFrame = BoidFrame(case_id)
    # optFrame = OptionFrame()  # Option frame disabled

    frame = 0
    number_of_rules = 2 # Alignment and cohesion that should be blended
    rule_picker = 0

    # Static target
    target = boidFrame.board.target    

    # Logging information
    log = Logger(case_id, test_id, flock_size)
    dst_target_log = np.zeros(flock_size)
    collision_tracker = 0


    # SPAWN BOIDS #####################################
    # Case c)
    if case_id == 'c':
        start_x = target[0]
        start_y = target[1]

        if flock_size == 1:
            flock = [Boid(boidFrame.board, start_x, start_y)]

        elif flock_size == 3:
            flock = [Boid(boidFrame.board, start_x-20, start_y), Boid(boidFrame.board, start_x+20, start_y), 
                     Boid(boidFrame.board, start_x, start_y+40)]
        
        elif flock_size == 7:
            flock = [Boid(boidFrame.board, start_x-30, start_y-30), Boid(boidFrame.board, start_x, start_y-30), Boid(boidFrame.board, start_x+30, start_y-30), 
                     Boid(boidFrame.board, start_x, start_y), 
                     Boid(boidFrame.board, start_x-30, start_y+30), Boid(boidFrame.board, start_x, start_y+30), Boid(boidFrame.board, start_x+30, start_y+30)]
        
        else:   # Default to 5
            flock = [Boid(boidFrame.board, start_x-20, start_y), Boid(boidFrame.board, start_x+20, start_y), 
                     Boid(boidFrame.board, start_x-20, start_y+40), Boid(boidFrame.board, start_x+20, start_y+40), 
                     Boid(boidFrame.board, start_x, start_y+20)]
        
        constants.FLOCK_SIZE = 5

    # Case d)
    elif case_id == 'd':
        start_x = target[0]
        start_y = 50
        flock = [Boid(boidFrame.board, start_x-20, start_y), Boid(boidFrame.board, start_x+20, start_y), 
                Boid(boidFrame.board, start_x-20, start_y+40), Boid(boidFrame.board, start_x+20, start_y+40), 
                Boid(boidFrame.board, start_x, start_y+20)]
        
        constants.FLOCK_SIZE = 5
        constants.GOALZONE = constants.DRONE_RADIUS * constants.FLOCK_SIZE + constants.DRONE_RADIUS
    
    # Default
    else:
        flock = [Boid(boidFrame.board, *np.random.rand(2) * constants.BOARD_SIZE) for _ in range(constants.FLOCK_SIZE)]

    steer = Behaviour(case_id, boidFrame.board.obstacleList_circle)  # Steering vector

    # MAIN LOOP #####################################
    while True:

        # Take screenshots every 50 frames, starting from frame 20 (to load gui)
        # if (frame % 50 + 20) == 20:
        #     takeScreenshot(boidFrame.board)

        # if frame == 100:
        #     takeScreenshot(boidFrame.board)
        
        # # Cursor position (dynamic target)
        # cursor_pos = [root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty()]
        # # target = cursor_pos
        
        rule_picker = (rule_picker + 1) % number_of_rules

        # Boid control
        for i, boid in enumerate(flock):
            change_tracker = boid.collision_flag

            if boid.collision_flag == False:
                steer.update(boid, flock, target, rule_picker)  # Steering vector

                if steer.force.__abs__() > constants.MAX_FORCE:
                    steer.force = (steer.force / steer.force.__abs__()) * constants.MAX_FORCE

                boid.update(steer.force)

            # Logging distance to egde of goalzone (0 while inside)
            dst_target_log[i] = max((boid.position - Vector2D(*target)).__abs__() - constants.GOALZONE, 0)

            collision_tracker += change_tracker != boid.collision_flag

        frame += 1

        # Main loop breakers
        if frame > frame_duration and frame_duration != -1: break
        if steer.break_flag == True: break

        if case_id == 'd': 
            log.log_to_file(frame, *dst_target_log)

        # Update GUI
        root.update_idletasks()
        root.update()
        time.sleep(0.01)


    if case_id == 'c': 
        log.log_to_file(test_id, frame, collision_tracker)

    root.destroy()

    return collision_tracker


if __name__ == '__main__':
    main(-1, 'd', 'main', constants.FLOCK_SIZE)
