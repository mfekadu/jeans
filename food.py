#!/usr/bin/env python3
from create_shapes import create_circle
from colors import *


def create_food():
    b, s = create_circle(r=10, bt='static')
    b.type = 'food'
    s.color = RED
    return b, s


if __name__ == "__main__":
    print(create_food())
