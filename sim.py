#!/usr/bin/env python3
# pylget for displaying to screen
from pyglet import window as p_window, app as p_app, clock as p_clock
from pymunk import Space  # for rigid body physics
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
from create_shapes import create_pentagon, create_triangle, create_segment
from create_shapes import create_circle, create_rect
from create_world import draw_border
from food import create_food
from bot import create_bot, move_bot
from rng import FOOD_X, FOOD_Y
import cfg
from sys import argv


def get_pymunk_space(gravity=(0, -9.807)):
    '''returns a `space` where the physics happens'''
    space = Space()
    # gravity is represented by a tuple
    # 0 acceleration in x-axis and -9.807 in y-axis
    space.gravity = gravity
    return space


# must be global because the @decorators work that way
window = p_window.Window(cfg.GW, cfg.GH, __file__, resizable=False)
space = get_pymunk_space(gravity=cfg.GRAVITY)
options = DrawOptions()
space.add(draw_border(cfg.GW, cfg.GH, thicc=cfg.BORDER_THICCNESS))


def begin_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("begin_collision", arbiter.shapes, space, data)
    return True


def pre_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("pre_collision", arbiter.shapes, space, data)
    return True


def post_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            space.remove(s1.body, s1) if s1.body.type == 'food' else space.remove(s2.body, s2)
            print("post_collision", arbiter.shapes, space, data)


def separate_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("separate_collision", arbiter.shapes, space, data)


handler = space.add_default_collision_handler()
handler.begin = begin_collision
handler.pre_solve = pre_collision
handler.post_solve = post_collision
handler.separate = separate_collision


def run():
    '''
    run the main loop for the game engine
    '''
    p_app.run()


def schedule(fun):
    '''
    given a function name
    tell pyglet to call that function every 1/60 seconds
    '''
    p_clock.schedule_interval(fun, 1.0/60)


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
        x = FOOD_X[i]
        y = FOOD_Y[i]
        food_body.position = (x, y)
        space.add(food_body, food_shape)

    assert len(space.shapes) == cfg.FOOD_COUNT + 4  # 4 borders and 100 food

    bot_body, bot_shape = create_bot()
    bot_body.position = (30, 70)
    space.add(bot_body, bot_shape)

    # do the update on 1/60th clock-ticks
    def update(dt):
        cfg.ITERATOR += 1
        print(cfg.ITERATOR) if cfg.DEBUG >= 2 else None
        quit(cfg.EXIT_SUCCESS) if cfg.ITERATOR >= cfg.MAX_STEPS else None
        if cfg.DEBUG >= 3:
            [print(type(shape), shape.body.position) for shape in space.shapes]
        # 4 borders + 1 bot + 100 food
        # assert len(space.shapes) == cfg.FOOD_COUNT + 5 if cfg.DEBUG else None
        for shape in space.shapes:
            x, y = shape.body.position.x, shape.body.position.y
            x_is_outside = (x < (0-10) or x > (cfg.GW+10))
            y_is_outside = (y < (0-10) or y > (cfg.GH+10))
            if (x_is_outside or y_is_outside):
                space.remove(shape, shape.body)
            else:
                if hasattr(shape.body, 'type'):
                    move_bot(shape.body) if shape.body.type == 'bot' else None
        return space.step(dt)

    schedule(update)

    run()


if __name__ == "__main__":
    if (len(argv) >= 2 and (argv[1] == '-d' or argv[1] == '--debug')):
        try:
            cfg.DEBUG = int(argv[2])
        except:
            print(cfg.USAGE)
            quit(cfg.EXIT_FAILURE)
    print("DEBUG LEVEL 1 - ASSERT STATEMENTS") if cfg.DEBUG else None
    print("DEBUG LEVEL 2 - PRINT STATEMENTS") if cfg.DEBUG >= 2 else None
    print("DEBUG LEVEL 3 - LOTS OF PRINTS") if cfg.DEBUG >= 3 else None
    main()
