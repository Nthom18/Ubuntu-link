'''
Global constants that are accessible to every script.

Author: Nicoline Louise Thomsen
'''

import pyautogui

_, SCREEN_HEIGHT = pyautogui.size()
# BOARD_SIZE = SCREEN_HEIGHT * 4/5
BOARD_SIZE = 864    # Board size of the computer used to run the tests


# Boids attributes
FLOCK_SIZE = 5
DRONE_RADIUS = 5
PERCEPTION = SCREEN_HEIGHT / 8
MAX_SPEED = 8
MAX_FORCE = 1
GOALZONE = DRONE_RADIUS * FLOCK_SIZE + DRONE_RADIUS

# Colours
COLOUR_RED = "red"
COLOUR_WHITE = "white"
COLOUR_GREY = "gray64"
COLOUR_DARKGREY = "gray25"
COLOUR_ORANGE = "DarkOrange1"
COLOUR_CORAL = "coral"

COLOUR_BOID = "IndianRed2"
COLOUR_OBSTACLE = "slateblue4"
COLOUR_CANVAS = "gray99"
COLOUR_GOAL = "spring green"
COLOUR_DEAD = "gray90"