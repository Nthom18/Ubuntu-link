import pyautogui

_, SCREEN_HEIGHT = pyautogui.size()
BOARD_SIZE = SCREEN_HEIGHT * 2/3

# Boids attributes
PERCEPTION = SCREEN_HEIGHT / 8
MAX_SPEED = 8
MAX_FORCE = 0.1

COLOUR_RED = "red"
COLOUR_WHITE = "white"