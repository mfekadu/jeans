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

def main():
    window = setup_window()
    #options = DrawOptions()

    # setup a Space for pymunk to do the fancy physics
    #space = pymunk.Space()
    #space.gravity = (0,-9.8)

    #body = pymunk.Body(1, 1666)

    run()

if __name__ == "__main__":
    print("hello world")
    main()
