#!/usr/bin/env python3
import pyglet  # for displaying to screen
import pymunk  # for rigid body physics
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
from create_shapes import create_pentagon, create_triangle, create_segment
from create_shapes import create_circle, create_rect
from create_world import draw_border
from food import create_food
from bot import create_bot
import numpy as np
import cfg

# set the seed for reproducability
np.random.seed(cfg.SEED)


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
BORDER_THICCNESS = 10

# must be global because the @decorators work that way
window = pyglet.window.Window(GW, GH, __file__, resizable=False)
space = get_pymunk_space(gravity=(0, -100))
options = DrawOptions()
space.add(draw_border(GW, GH, thicc=BORDER_THICCNESS))

# the space that food and bots can spawn
IGW = GW - (BORDER_THICCNESS * 2)  # inner game width
IGH = GH - (BORDER_THICCNESS * 2)  # inner game height


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

    # initialize food at random places
    for i in range(cfg.FOOD_COUNT):
        food_body, food_shape = create_food()
        x = np.random.randint(BORDER_THICCNESS, IGW)
        y = np.random.randint(BORDER_THICCNESS, IGH)
        food_body.position = (x, y)
        space.add(food_body, food_shape)

    assert len(space.shapes) == cfg.FOOD_COUNT + 4  # 4 borders and 100 food

    bot_body, bot_shape = create_bot()
    bot_body.position = (30, 70)
    space.add(bot_body, bot_shape)

    # do the update on 1/60th clock-ticks
    def update(dt):
        if cfg.DEBUG > 1:
            [print(type(shape), shape.body.position) for shape in space.shapes]
        # 4 borders + 1 bot + 100 food
        assert len(space.shapes) == cfg.FOOD_COUNT + 5 if cfg.DEBUG else None
        for shape in space.shapes:
            x, y = shape.body.position.x, shape.body.position.y
            if (x < (0-10) or x > (GW+10) or y < (0-10) or y > (GH+10)):
                space.remove(shape, shape.body)
        return space.step(dt)

    schedule(update)

    run()


if __name__ == "__main__":
    print("DEBUG LEVEL 1 - ASSERT STATEMENTS") if cfg.DEBUG else None
    print("DEBUG LEVEL 2 - PRINT STATEMENTS") if cfg.DEBUG > 1 else None
    main()
