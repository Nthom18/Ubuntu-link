'''
Global constants that are accessible to every script.

Author: Nicoline Louise Thomsen
'''
GAZEBO_SCALE = 0.074

# import pyautogui

# _, SCREEN_HEIGHT = pyautogui.size()
# BOARD_SIZE = SCREEN_HEIGHT * 4/5
SCREEN_HEIGHT = 1080 * GAZEBO_SCALE
BOARD_SIZE = 864 * GAZEBO_SCALE    # Board size of the computer used to run the tests


# Boids attributes
FLOCK_SIZE = 5
DRONE_RADIUS = 0.74
PERCEPTION = SCREEN_HEIGHT / 8
MAX_SPEED = 1
MAX_FORCE = 1
GOALZONE = DRONE_RADIUS * FLOCK_SIZE + DRONE_RADIUS

# Physics simulation specific:
OBSTACLE_LIST= [[8.732, -33.3, 2.22], [-11.248, -32.56, 2.22], [-19.018, -37, 2.22], [-9.768, -22.2, 2.96], [-17.168, -14.8, 3.7], [5.032, -18.5, 3.7], [19.832, -29.6, 5.18], [-5.328, -37, 5.55], [-138.158, -31.968, 111], [138.158, -31.968, 111]]

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
