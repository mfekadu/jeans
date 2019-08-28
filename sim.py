#!/usr/bin/env python3

import pyglet # for displaying to screen
import pymunk # for rigid body physics
from pymunk.pyglet_util import DrawOptions # idk what this is

# game width and height
GW = 800
GH = 800

def setup_window():
    '''
    setup the pyglet window
    '''
    return pyglet.window.Window(GW, GH, __file__, resizable=False)

def run():
    '''
    run the main loop for the game engine
    '''
    pyglet.app.run()

def update(dt):
    pass

def schedule(fun):
    '''
    given a function name
    tell pyglet to call that function every 1/60 seconds
    '''
    pyglet.clock.schedule_interval(fun, 1.0/60)


def main():
    window = setup_window()
    
    # do the update on 1/60th clock-ticks
    schedule(update)

    #options = DrawOptions()

    # setup a Space for pymunk to do the fancy physics
    #space = pymunk.Space()
    #space.gravity = (0,-9.8)

    #body = pymunk.Body(1, 1666)

    run()

if __name__ == "__main__":
    print("hello world")
    main()
