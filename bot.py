#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *
from cfg import *


def create_bot():
    b, s = create_circle(r=BOT_RADIUS, bt='dynamic')
    b.type = 'bot'
    s.color = BOT_COLOR
    return b, s


if __name__ == "__main__":
    print(create_bot())
    print(create_bot()[0].type)
    print(create_bot()[1].color)
