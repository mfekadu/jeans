#!/usr/bin/env python3
# pylget for displaying to screen
from pyglet import window as p_window, app as p_app, clock as p_clock
from pyglet.window import key
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
import pickle
from os.path import join
from os import mkdir
from time import time, timezone

SIM_NAME = 'sim' + '_' + str(time()) + '_' + str(timezone)
mkdir(join(cfg.DUMPS_DIR, SIM_NAME))

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
            print("begin_collision", arbiter.shapes, space, data) if cfg.DEBUG >= 2 else None
    return True


def pre_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("pre_collision", arbiter.shapes, space, data) if cfg.DEBUG >= 2 else None
    return True


def post_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            space.remove(s1.body, s1) if s1.body.type == 'food' else space.remove(s2.body, s2)
            print("post_collision", arbiter.shapes, space, data) if cfg.DEBUG >= 2 else None


def separate_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("separate_collision", arbiter.shapes, space, data) if cfg.DEBUG >= 2 else None


handler = space.add_default_collision_handler()
handler.begin = begin_collision
handler.pre_solve = pre_collision
handler.post_solve = post_collision
handler.separate = separate_collision


bot_body, bot_shape = create_bot()


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
    p_clock.schedule_interval(fun, cfg.PY_STEP)

hold = False
last_move = cfg.MOVE_STOP


@window.event
def on_key_press(symbol, modifiers):
    global hold, last_move
    if symbol == key.UP:
        hold = True
        move_bot(bot_body, r=cfg.MOVE_UP)
        last_move = cfg.MOVE_UP
    elif symbol == key.DOWN:
        move_bot(bot_body, r=cfg.MOVE_DOWN)
        last_move = cfg.MOVE_DOWN
        hold = True
    elif symbol == key.RIGHT:
        move_bot(bot_body, r=cfg.MOVE_RIGHT)
        last_move = cfg.MOVE_RIGHT
        hold = True
    elif symbol == key.LEFT:
        move_bot(bot_body, r=cfg.MOVE_LEFT)
        last_move = cfg.MOVE_LEFT
        hold = True
    # else:
    print("PRESS", "symbol", symbol, "modifier", modifiers)


@window.event
def on_key_release(symbol, modifiers):
    global hold
    if symbol in (key.UP, key.DOWN, key.LEFT, key.RIGHT):
        hold = False
    print("RELEASE", "symbol", symbol, "modifier", modifiers)


@window.event
def on_draw():
    '''
    stuff that happens when pyglet is drawing
    '''
    window.clear()  # start with a clean window
    space.debug_draw(options)


def init_food(N=0, s=None, food_x=[], food_y=[]):
    '''
    given a food count N, a pymunk Space s, a list of x-positions,
          and a list of y-positions.
    mutate the space s by adding N food.
    return True everything went okay.
    '''
    assert N > 0, "bad inputs - expected to initialize at least 1 food"
    assert len(food_x) == len(food_y) == N, "bad inputs"
    assert s, "please pass a reference to the Pymunk.Space"
    assert type(s) == Space  # pymunk.space.Space

    for i in range(N):
        food_body, food_shape = create_food()
        x = food_x[i]
        y = food_y[i]
        food_body.position = (x, y)
        s.add(food_body, food_shape)

    return True


'''
Advice from WesleyAC:
Avoid global "space" object by creating some sort of local scope such that you
  can pass in a function to mutate the space, but the space itself
  remains... encapsulated?
  Yeah, that sounds like I should make a wrapper class around space
  Also, that could be function which accepts a function as an argument.
Also, python function arguments are "pass by refernce" and not "by value"
  https://stackoverflow.com/a/22559153/5411712
  So, it's totally fine to make a function that takes a space and mutates it,
  because that's how pymunk is designed to work anyway.
'''

def main():
    '''
    main is where all the magic happens.

    '''
    # make sure window and space are a thing
    assert window
    assert space

    # initialize food at random places
    init_food(cfg.FOOD_COUNT, space, FOOD_X, FOOD_Y)

    assert len(space.shapes) == cfg.FOOD_COUNT + 4  # 4 borders and 100 food

    bot_body.position = (50, 100)
    space.add(bot_body, bot_shape)

    # 4 borders + 1 bot + 100 food
    assert len(space.shapes) == cfg.FOOD_COUNT + 5 if cfg.DEBUG else None
    print(len(space.shapes))

    # do the update on 1/60th clock-ticks
    def update(dt):
        cfg.ITERATOR += 1
        print(cfg.ITERATOR) if cfg.DEBUG >= 2 else None
        quit(cfg.EXIT_SUCCESS) if cfg.ITERATOR >= cfg.MAX_STEPS else None
        if cfg.DEBUG >= 3:
            [print(type(shape), shape.body.position) for shape in space.shapes]

        if hold:
            move_bot(bot_body, r=last_move)

        for shape in space.shapes:
            x, y = shape.body.position.x, shape.body.position.y
            x_is_outside = (x < (0-10) or x > (cfg.GW+10))
            y_is_outside = (y < (0-10) or y > (cfg.GH+10))
            if (x_is_outside or y_is_outside):
                space.remove(shape, shape.body)
            # else:
            #     if hasattr(shape.body, 'type'):
            #         move_bot(shape.body) if shape.body.type == 'bot' else None

        new_dump_filename = 'space_and_cfg_dump' + '_'
        new_dump_filename += 'v' + str(cfg.VERSION) + '_'
        new_dump_filename += str(time()) + '_'  + str(timezone) + '_'
        new_dump_filename += str(cfg.ITERATOR) + '_'
        new_dump_filename += '.pickle'
        make_var_val_tup = lambda i: (i, str(cfg.__getattribute__(i)))
        cfg_attrs = dict(make_var_val_tup(item) for item in dir(cfg) if not item.startswith('__'))
        with open( join(cfg.DUMPS_DIR, SIM_NAME, new_dump_filename), 'wb' ) as f:
            pickle.dump([space, cfg_attrs], f)
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
