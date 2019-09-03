#!/usr/bin/env python3
'''
rng.py - Random Number Generator

This file will contain randomly generated numpy arrays using cfg.SEED
    so that the random numbers are consistent throughout each run.

Random numbers are used for making choices in the simulation (e.g move(bot)).

Hopefully setting seed once in this file and generating all the random numbers
    once in this file, will lead to consistent/predictable results.
'''
import cfg
from numpy import random as np_random

# set the seed for reproducability
print(np_random.get_state()[1][0], "??", 42)
np_random.seed(cfg.SEED)
print(np_random.get_state()[1][0], "??", 42)

# array for the bot moves
# MOVES = np_random.randint(0, cfg.MOVE_OPTIONS, cfg.MAX_STEPS)
MOVES = [0] * 20 + [1] * 25 + [3] * 25 + [2] * 25 + [4]*25

# arrays for the food positions
FOOD_X = np_random.randint(low=cfg.BORDER_THICCNESS, high=cfg.IGW,
                           size=cfg.FOOD_COUNT)
FOOD_Y = np_random.randint(low=cfg.BORDER_THICCNESS, high=cfg.IGH,
                           size=cfg.FOOD_COUNT)
