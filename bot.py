#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *
import cfg
from rng import MOVES


def move_0(bot_body):
    bot_body.velocity = (0, 0)


def move_forward(bot_body):
    bot_body.velocity = (0, 200)


def move_backward(bot_body):
    bot_body.velocity = (0, -25)


def move_right(bot_body):
    bot_body.velocity = (250, 0)


def move_left(bot_body):
    bot_body.velocity = (-25, 0)


def move_bot(bot_body):
    # print(np_random.get_state()[1][0], "??", 42)
    print("move_bot", "cfg.ITERATOR", cfg.ITERATOR) if cfg.DEBUG >= 2 else None
    r = MOVES[cfg.ITERATOR]
    if r == 1:
        move_forward(bot_body)
    elif r == 2:
        move_backward(bot_body)
    elif r == 3:
        move_right(bot_body)
    elif r == 4:
        move_left(bot_body)
    else:
        move_0(bot_body)


def create_bot():
    b, s = create_circle(r=cfg.BOT_RADIUS, bt='dynamic')
    b.type = 'bot'
    s.color = cfg.BOT_COLOR
    return b, s


if __name__ == "__main__":
    print(create_bot())
    print(create_bot()[0].type)
    print(create_bot()[1].color)
