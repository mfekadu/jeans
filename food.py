#!/usr/bin/env python3
from create_shapes import create_circle
from cfg import *


def create_food():
    # TODO: consider static/kinematic food that can only be moved via "grab"
    b, s = create_circle(r=FOOD_RADIUS, bt='dynamic')
    b.type = 'food'
    s.color = FOOD_COLOR
    return b, s


if __name__ == "__main__":
    print(create_food())
    print(create_food()[0].type)
    print(create_food()[1].color)
