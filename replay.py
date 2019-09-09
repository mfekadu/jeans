#!/usr/bin/env python3
from pyglet import window as p_window, app as p_app, clock as p_clock
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction
from pyglet.window import key as p_key
from pickle import load as pickle_load
from os.path import join as path_join
from os import listdir as os_listdir
import argparse


'''
These 4 functions below are just defined to keep python happy
    because the "space" inside the pickle dump
    references these funcitons as if they exist in __main__
'''


def begin_collision(a, s, d): return True


def pre_collision(a, s, d): return True


def post_collision(a, s, d): return None


def separate_collision(a, s, d): return None


def get_pickle_filepaths(dumps_dir):
    fnames = os_listdir(dumps_dir)
    fnames.remove('.DS_Store') if '.DS_Store' in fnames else None
    fpaths = [path_join(dumps_dir, fn) for fn in fnames]
    fpaths.sort()
    return fpaths


# GLOBAL Variables
space = None
cfg = None
window = None
cfg_GW = 0
cfg_GH = 0
cfg_ITERATOR = 0
FILEPATHS = []


def read_pickle_file_and_save_to_global_variables(filepath):
    global space, cfg
    with open(filepath, 'rb') as f:
        space, cfg = pickle_load(f)


def update(dt):
    global cfg_ITERATOR
    if cfg_ITERATOR >= len(FILEPATHS):
        print("End of simulation.", "Goodbye!")
        quit()

    if cfg_ITERATOR <= 0:
        cfg_ITERATOR = 0

    fpath = FILEPATHS[cfg_ITERATOR % len(FILEPATHS)]
    read_pickle_file_and_save_to_global_variables(fpath)

    space.step(dt)


def main():
    assert window
    assert space

    p_clock.schedule_interval(update, float(cfg['PY_STEP']))
    p_app.run()


if __name__ == "__main__":
    print("\n")
    DESC = 'replay Pickle dumps of Pymunk'
    DUMPS_HELP = 'the directory containing the .pickle files'
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('dumps_dir', metavar='dumps_dir',
                        type=str, nargs=1, help=DUMPS_HELP)
    args = parser.parse_args()
    DUMPS_DIR = args.dumps_dir[0]

    FILEPATHS = get_pickle_filepaths(DUMPS_DIR)
    read_pickle_file_and_save_to_global_variables(FILEPATHS[0])

    assert space
    assert cfg
    assert FILEPATHS
    assert cfg.keys
    assert len(cfg.keys()) > 0

    cfg_GW = int(cfg['GW'])
    cfg_GH = int(cfg['GH'])
    cfg_ITERATOR = int(cfg['ITERATOR'])
    window = p_window.Window(cfg_GW, cfg_GH, __file__, resizable=False)
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
        global cfg_ITERATOR
        if motion == p_key.MOTION_UP:
            cfg_ITERATOR += 10
        elif motion == p_key.MOTION_DOWN:
            cfg_ITERATOR -= 10
        elif motion == p_key.MOTION_RIGHT:
            cfg_ITERATOR += 1
        elif motion == p_key.MOTION_LEFT:
            cfg_ITERATOR -= 1

    main()
