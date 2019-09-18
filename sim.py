#!/usr/bin/env python3
# pylget for displaying to screen
from pyglet import window as p_window, app as p_app, clock as p_clock
from pyglet.window import key as p_key
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


def get_pymunk_space(gravity=(0, -9.807)):
    '''returns a `space` where the physics happens'''
    space = Space()
    # gravity is represented by a tuple
    # 0 acceleration in x-axis and -9.807 in y-axis
    space.gravity = gravity
    return space


def begin_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("begin_collision", arbiter.shapes,
                  space, data) if cfg.DEBUG >= 2 else None
    return True


def pre_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("pre_collision", arbiter.shapes, space,
                  data) if cfg.DEBUG >= 2 else None
    return True


def post_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            space.remove(s1.body, s1) if s1.body.type == 'food' else space.remove(
                s2.body, s2)
            print("post_collision", arbiter.shapes,
                  space, data) if cfg.DEBUG >= 2 else None


def separate_collision(arbiter, space, data):
    s1 = arbiter.shapes[0]
    s2 = arbiter.shapes[1]
    if hasattr(s1.body, 'type') and hasattr(s2.body, 'type'):
        types = [s1.body.type, s2.body.type]
        if ('bot' in types):
            print("separate_collision", arbiter.shapes,
                  space, data) if cfg.DEBUG >= 2 else None


def run():
    '''run the main loop for the game engine'''
    p_app.run()


def schedule(fun):
    '''
    given a function name
    tell pyglet to call that function every 1/60 seconds
    '''
    p_clock.schedule_interval(fun, cfg.PY_STEP)


def add_food_to_space(s=None, N=0, xs=[], ys=[]):
    '''
    Given a food count `N`, a pymunk Space `s`, a list of x-positions `xs`,
          and a list of y-positions `ys`.

    Mutate the space `s` by adding `N` food.

    Return True if everything went okay.
    '''
    assert N > 0, "bad inputs - expected to initialize at least 1 food"
    assert len(xs) == len(ys) == N, "bad inputs"
    assert s, "please pass a reference to the Pymunk.Space"
    assert type(s) == Space  # pymunk.space.Space

    for i in range(N):
        food_body, food_shape = create_food()
        x = xs[i]
        y = ys[i]
        food_body.position = (x, y)
        s.add(food_body, food_shape)

    return True


def add_bots_to_space(s=None, N=0, xs=[], ys=[]):
    '''
    Given a bot count `N`, a pymunk Space `s`, a list of x-positions `xs`,
          and a list of y-positions `ys`.

    Mutate the space `s` by adding `N` bots.

    Return True if everything went okay.
    '''
    assert N > 0, "bad inputs - expected to initialize at least 1 bot"
    assert len(xs) == len(ys) == N, "bad inputs"
    assert s, "please pass a reference to the Pymunk.Space"
    assert type(s) == Space  # pymunk.space.Space
    # TODO: make a for loop here
    bot_body, bot_shape = create_bot()
    bot_body.position = (50, 100)
    s.add(bot_body, bot_shape)
    return bot_body


def save_data(space, sim_name):
    new_save_filename = 'space_and_cfg_save' + '_'
    new_save_filename += 'v' + str(cfg.VERSION) + '_'
    new_save_filename += str(time()) + '_' + str(timezone) + '_'
    new_save_filename += str(cfg.ITERATOR) + '_'
    new_save_filename += '.pickle'
    def make_var_val_tup(i): return (i, str(cfg.__getattribute__(i)))
    cfg_attrs = dict(make_var_val_tup(item)
                     for item in dir(cfg) if not item.startswith('__'))
    with open(join(cfg.SAVES_DIR, sim_name, new_save_filename), 'wb') as f:
        pickle.dump([space, cfg_attrs], f)


def keep_shapes_in_bounds(space):
    for shape in space.shapes:
        x, y = shape.body.position.x, shape.body.position.y
        x_is_outside = (x < (0-10) or x > (cfg.GW+10))
        y_is_outside = (y < (0-10) or y > (cfg.GH+10))
        if (x_is_outside or y_is_outside):
            space.remove(shape, shape.body)
        # else:
        #     if hasattr(shape.body, 'type'):
        #         move_bot(shape.body) if shape.body.type == 'bot' else None



def main():
    '''main is where all the magic happens.'''
    SIM_NAME = 'sim' + '_' + str(time()) + '_' + str(timezone)
    mkdir(join(cfg.SAVES_DIR, SIM_NAME))

    # initialize pyglet window
    window = p_window.Window(cfg.GW, cfg.GH, __file__, resizable=False)

    # initialize pymunk space with borders
    space = get_pymunk_space(gravity=cfg.GRAVITY)
    space.add(draw_border(cfg.GW, cfg.GH, thicc=cfg.BORDER_THICCNESS))

    # initialize collision handler
    handler = space.add_default_collision_handler()
    handler.begin = begin_collision
    handler.pre_solve = pre_collision
    handler.post_solve = post_collision
    handler.separate = separate_collision

    # initialize food at random places
    bot_body = add_food_to_space(space, cfg.FOOD_COUNT, FOOD_X, FOOD_Y)
    assert (len(space.shapes) == cfg.FOOD_COUNT + 4)  # 4 borders and 100 food

    # initialize the bots
    bot_body = add_bots_to_space(space, 1, [50], [100])
    # 4 borders + 1 bot + 100 food
    if cfg.DEBUG:
        assert (len(space.shapes) == cfg.FOOD_COUNT + 5)

    # https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/
    #         programming_guide/events.html
    # add event handlers to the window
    # window.push_handlers(on_draw)
    # TODO: remove this function because the simulation should not be controllable
    def on_text_motion(motion):
        if motion == p_key.MOTION_UP:
            move_bot(bot_body, r=cfg.MOVE_UP)
        elif motion == p_key.MOTION_DOWN:
            move_bot(bot_body, r=cfg.MOVE_DOWN)
        elif motion == p_key.MOTION_RIGHT:
            move_bot(bot_body, r=cfg.MOVE_RIGHT)
        elif motion == p_key.MOTION_LEFT:
            move_bot(bot_body, r=cfg.MOVE_LEFT)

    options = DrawOptions()

    def on_draw():
        '''stuff that happens when pyglet is drawing'''
        window.clear()  # start with a clean window
        space.debug_draw(options)

    window.on_draw = on_draw
    window.on_text_motion = on_text_motion

    # do the update on 1/60th clock-ticks
    def update(dt):
        cfg.ITERATOR += 1
        print(cfg.ITERATOR) if cfg.DEBUG >= 2 else None

        quit(cfg.EXIT_SUCCESS) if cfg.ITERATOR >= cfg.MAX_STEPS else None

        if cfg.DEBUG >= 3:
            [print(type(shape), shape.body.position) for shape in space.shapes]

        keep_shapes_in_bounds(space)

        save_data(space, SIM_NAME) if cfg.ITERATOR % 10 == 0 else None

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
