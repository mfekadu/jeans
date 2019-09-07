#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *
import cfg
from rng import MOVES


def is_out_of_bounds(pos):
    ''' given position tuple, return True if out of bounds else False '''
    x_oob = (pos[0] > cfg.IGW) or (pos[0] < cfg.BORDER_THICCNESS)
    y_oob = (pos[1] > cfg.IGH) or (pos[1] < cfg.BORDER_THICCNESS)
    return x_oob or y_oob


def safely_update_velocity(new_vel, bot_x, bot_y):
    '''
    given a new velocity, and bot's current x & y position
    return new_vel if bot stays in bounds, else (0,0)
    '''
    # new_x <px/frame> = X <px> + (V <px/sec> * PY_STEP <sec/frame>)
    new_x = bot_x + new_vel[0] * (cfg.PY_STEP)
    new_y = bot_y + new_vel[1] * (cfg.PY_STEP)
    new_pos = (new_x, new_y)
    if is_out_of_bounds(new_pos):
        return (0,0)

    return new_vel

def move_0(bot_body):
    bot_body.velocity = (0, 0)


def move_forward(bot_body):
    # _____
    #   .  |
    #      |

    # TODO: do the magic math stuff
    # so that it works
    # near the edge :)
    proposed_velocity = (0, 2000)
    x = bot_body.position.x
    y = bot_body.position.y
    bot_body.velocity = safely_update_velocity(proposed_velocity, x, y)


def move_backward(bot_body):
    # bot_body.velocity = (0, -200)
    proposed_velocity = (0, 2000)
    x = bot_body.position.x
    y = bot_body.position.y
    bot_body.velocity = safely_update_velocity(proposed_velocity, x, y)


def move_right(bot_body):
    # bot_body.velocity = (200, 0)
    proposed_velocity = (2000, 0)
    x = bot_body.position.x
    y = bot_body.position.y
    bot_body.velocity = safely_update_velocity(proposed_velocity, x, y)


def move_left(bot_body):
    # bot_body.velocity = (-200, 0)
    proposed_velocity = (2000, 0)
    x = bot_body.position.x
    y = bot_body.position.y
    bot_body.velocity = safely_update_velocity(proposed_velocity, x, y)


def move_bot(bot_body, r=None):
    print("bot_vel", bot_body.velocity)
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
    s.elasticity = cfg.BOT_ELASTICITY
    s.color = cfg.BOT_COLOR
    return b, s


if __name__ == "__main__":
    print(create_bot())
    print(create_bot()[0].type)
    print(create_bot()[1].color)
