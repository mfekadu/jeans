#!/usr/bin/env python3
import pyglet  # for displaying to screen
import pymunk  # for rigid body physics
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
from create_shapes import create_pentagon, create_triangle, create_segment
from create_shapes import create_circle, create_rect
from create_world import draw_border
from food import create_food
from bot import create_bot
from colors import *


def get_pymunk_space(gravity=(0, -9.807)):
    '''returns a `space` where the physics happens'''
    space = pymunk.Space()
    # gravity is represented by a tuple
    # 0 acceleration in x-axis and -9.807 in y-axis
    space.gravity = gravity
    return space


# game width and height
GW = 400
GH = 400
# must be global because the @decorators work that way
window = pyglet.window.Window(GW, GH, __file__, resizable=False)
space = get_pymunk_space(gravity=(0, -100))
options = DrawOptions()
space.add(draw_border(GW, GH))


def run():
    '''
    run the main loop for the game engine
    '''
    pyglet.app.run()


def schedule(fun):
    '''
    given a function name
    tell pyglet to call that function every 1/60 seconds
    '''
    pyglet.clock.schedule_interval(fun, 1.0/60)


@window.event
def on_draw():
    '''
    stuff that happens when pyglet is drawing
    '''
    window.clear()  # start with a clean window
    space.debug_draw(options)


def main():
    # make sure window and space are a thing
    assert window
    assert space

    body, shape = create_rect(x=350, y=300, scalar=50)
    shape.color = RED
    space.add(body, shape)

    cbody, cshape = create_circle(r=50, x=400, y=400)
    space.add(cbody, cshape)

    line_body, line_shape = create_segment(x=600, y=600, scalar=50)
    space.add(line_body, line_shape)

    tbody, tshape = create_triangle(x=100, y=600, scalar=50)
    space.add(tbody, tshape)

    pb, ps = create_pentagon(x=150, y=150, scalar=50)
    space.add(pb, ps)

    food_body, food_shape = create_food()
    food_body.position = (30, 30)
    space.add(food_body, food_shape)

    bot_body, bot_shape = create_bot()
    bot_body.position = (30, 70)
    space.add(bot_body, bot_shape)

    # do the update on 1/60th clock-ticks
    def update(dt):
        [print(type(shape), shape.body.position) for shape in space.shapes]
        for shape in space.shapes:
            x, y = shape.body.position.x, shape.body.position.y
            if (x < (0-10) or x > (GW+10) or y < (0-10) or y > (GH+10)):
                space.remove(shape, shape.body)
        return space.step(dt)

    schedule(update)

    run()


if __name__ == "__main__":
    print("hello world")
    main()
