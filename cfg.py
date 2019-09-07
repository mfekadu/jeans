#!/usr/bin/env python3
'''
A place to store global variables to customize and configure the simulation.
'''
import colors


# ******************************************************************************
# Constants for random generators
# ******************************************************************************
SEED = 42  # set the seed for random number generators for reproducability

MOVE_OPTIONS = 5  # move_0, move_up, move_down, move_left, move_right

ITERATOR = 0  # keeps track of how many steps/frames pyglet has looped over

MAX_STEPS = 1000000  # 1 million is the arbitrary limit


# ******************************************************************************
# Constants for engines (pymunk/pyglet)
# ******************************************************************************
# parameters of the window
GW = 400  # game width
GH = 400  # game height
BORDER_THICCNESS = 10


# the space within the window that food and bots can spawn
IGW = GW - (BORDER_THICCNESS * 2)  # inner game width
IGH = GH - (BORDER_THICCNESS * 2)  # inner game height

GRAVITY = (0, 0)


# ******************************************************************************
# Constants for debugging
# ******************************************************************************
# DEBUG can optionally be set to:
#    False/0 (no-debug), 1 (asserts), 2 (prints), 3 (lots of prints)
DEBUG = True

USAGE = "usage: python3 sim.py [-d [0, 1, 2]]"
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# ******************************************************************************
# Constants for the simulation (bots, food, etc)
# ******************************************************************************
FOOD_COUNT = 100
FOOD_RADIUS = 5
FOOD_COLOR = colors.RED
# FOOD_ELASTICITY = 0.0

BOT_RADIUS = 10
BOT_COLOR = colors.YELLOW
BOT_ELASTICITY = 0.98

MOVE_STOP = 0
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4

WALL_ELASTICITY = 0.98