#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *
import cfg
from numpy import random as np_random

# set the seed for reproducability
print(np_random.get_state()[1][0], "??", 42)
np_random.seed(cfg.SEED)
print(np_random.get_state()[1][0], "??", 42)
# mil = 1000000
# np.random.randint(1,5,(1000,mil))


def move_forward(bot_body):
    bot_body.velocity = (0, 250)


def move_backward(bot_body):
    bot_body.velocity = (0, -250)


def move_right(bot_body):
    bot_body.velocity = (250, 0)


def move_left(bot_body):
    bot_body.velocity = (-250, 0)


def move_bot(bot_body):
    print(np_random.get_state()[1][0], "??", 42)
    r = np_random.rand()
    if r >= 0.7:
        move_forward(bot_body)
    elif r <= 0.3:
        move_backward(bot_body)
    elif r > 0.5:
        move_right(bot_body)
    else:
        move_left(bot_body)


def create_bot():
    b, s = create_circle(r=cfg.BOT_RADIUS, bt='dynamic')
    b.type = 'bot'
    s.color = cfg.BOT_COLOR
    return b, s


if __name__ == "__main__":
    print(create_bot())
    print(create_bot()[0].type)
    print(create_bot()[1].color)
