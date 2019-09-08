#!/usr/bin/env python3
from pyglet import window as p_window, app as p_app, clock as p_clock
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
import cfg
from pickle import load
from os.path import join
from os import listdir
from create_world import draw_border

window = p_window.Window(cfg.GW, cfg.GH, __file__, resizable=False)


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



fname = 'space_dump_1567943406.325641_18000_1_.pickle'
dumps = listdir(cfg.DUMPS_DIR)
dumps.sort()
dumps.remove('.DS_Store') if '.DS_Store' in dumps else None
[dumps.remove(n) for n in dumps if n[-4:] == '.zip']

fnames = listdir(join(cfg.DUMPS_DIR,dumps[0]))
fnames = [join(dumps[0], fn) for fn in fnames]
fnames.sort()
fnames.remove('.DS_Store') if '.DS_Store' in fnames else None
#assert fnames[0] == fname, "{} != {}".format(fnames[0], fname)

with open( join(cfg.DUMPS_DIR, fnames[0]), 'rb') as f:
    space = load(f)

options = DrawOptions()
space.add(draw_border(cfg.GW, cfg.GH, thicc=cfg.BORDER_THICCNESS))



handler = space.add_default_collision_handler()
handler.begin = begin_collision
handler.pre_solve = pre_collision
handler.post_solve = post_collision
handler.separate = separate_collision




@window.event
def on_draw():
    '''
    stuff that happens when pyglet is drawing
    '''
    window.clear()  # start with a clean window
    space.debug_draw(options)


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


def main():
    global space
    assert window
    assert space
    print("space", space)

    def update(dt):
        global space
        cfg.ITERATOR += 1
        print(dt)
        foo = space
        with open( join(cfg.DUMPS_DIR, fnames[cfg.ITERATOR]), 'rb') as f:
            space = load(f)
        space.step(dt)

    schedule(update)
    run()


if __name__ == "__main__":
    main()

