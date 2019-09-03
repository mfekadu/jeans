#!/usr/bin/env python3
'''
A place to store global variables to customize and configure the simulation.
'''
import colors

SEED = 42  # set the seed for random number generators for reproducability

DEBUG = True  # optionally set to False/0 (no-debug), 1 (asserts), 2 (prints)

GRAVITY = (0, 0)

FOOD_COUNT = 100
FOOD_RADIUS = 5
FOOD_COLOR = colors.RED


BOT_RADIUS = 10
BOT_COLOR = colors.BLUE
