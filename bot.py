#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *
import cfg
from rng import MOVES


def move_0(bot_body):
    bot_body.velocity = (0, 0)


def move_forward(bot_body):

    # _____
    #   .  |
    #      |

    # TODO: do the magic math stuff so that it works near the edge :)


    bot_body.velocity = (0, 200)


def move_backward(bot_body):
    bot_body.velocity = (0, -200)


def move_right(bot_body):
    bot_body.velocity = (200, 0)


def move_left(bot_body):
    bot_body.velocity = (-200, 0)


def move_bot(bot_body, r=None):
    r = MOVES[cfg.ITERATOR % len(MOVES)] if r is None else r
    # print(np_random.get_state()[1][0], "??", 42)
    print("move_bot", "cfg.ITERATOR", cfg.ITERATOR) if cfg.DEBUG >= 2 else None

    print("move_bot", r, cfg.ITERATOR)

    if r == cfg.MOVE_UP:
        move_forward(bot_body)
    elif r == cfg.MOVE_DOWN:
        move_backward(bot_body)
    elif r == cfg.MOVE_RIGHT:
        move_right(bot_body)
    elif r == cfg.MOVE_LEFT:
        move_left(bot_body)
    else:
        move_0(bot_body)


def create_bot():
    b, s = create_circle(r=cfg.BOT_RADIUS, bt='dynamic')
    b.type = 'bot'
    s.elasticity = 0.98
    s.color = cfg.BOT_COLOR
    return b, s


if __name__ == "__main__":
    print(create_bot())
    print(create_bot()[0].type)
    print(create_bot()[1].color)
