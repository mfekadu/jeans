#!/usr/bin/env python3
from pyglet import window as p_window, app as p_app, clock as p_clock
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
from pyglet.window import key as p_key
import cfg
from pickle import load as pickle_load
from os.path import join as path_join
from os import listdir as os_listdir
from create_world import draw_border

window = p_window.Window(cfg.GW, cfg.GH, __file__, resizable=False)

'''
These 4 functions below are just defined to keep python happy
    because the "space" inside the pickle dump
    references these funcitons as if they exist in __main__
'''


def begin_collision(a, s, d): return True


def pre_collision(a, s, d): return True


def post_collision(a, s, d): return None


def separate_collision(a, s, d): return None


dumps = os_listdir(cfg.DUMPS_DIR)
dumps.sort()
dumps.remove('.DS_Store') if '.DS_Store' in dumps else None
dumps = [d for d in dumps if d[-3:] != 'zip']

fnames = os_listdir(path_join(cfg.DUMPS_DIR, dumps[0]))
fnames = [path_join(dumps[0], fn) for fn in fnames]
fnames.sort()
fnames.remove('.DS_Store') if '.DS_Store' in fnames else None

with open(path_join(cfg.DUMPS_DIR, fnames[0]), 'rb') as f:
    space = pickle_load(f)

options = DrawOptions()


@window.event
def on_draw():
    '''
    stuff that happens when pyglet is drawing
    '''
    window.clear()  # start with a clean window
    space.debug_draw(options)


@window.event
def on_text_motion(motion):
    if motion == p_key.MOTION_UP:
        cfg.ITERATOR += 10
    elif motion == p_key.MOTION_DOWN:
        cfg.ITERATOR -= 10
    elif motion == p_key.MOTION_RIGHT:
        cfg.ITERATOR += 1
    elif motion == p_key.MOTION_LEFT:
        cfg.ITERATOR -= 1


def update(dt):
    global space
    if cfg.ITERATOR >= len(fnames):
        print("End of simulation.", "Goodbye!")
        quit()

    if cfg.ITERATOR <= 0:
        cfg.ITERATOR = 0

    fname = fnames[cfg.ITERATOR % len(fnames)]
    with open(path_join(cfg.DUMPS_DIR, fname), 'rb') as f:
        space = pickle_load(f)
    space.step(dt)


def main():
    assert window
    assert space

    p_clock.schedule_interval(update, cfg.PY_STEP)
    p_app.run()


if __name__ == "__main__":
    main()
