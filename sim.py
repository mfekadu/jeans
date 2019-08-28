#!/usr/bin/env python3

import pyglet # for displaying to screen
import pymunk # for rigid body physics
from pymunk.pyglet_util import DrawOptions # pymunk/pyglet interaction


def get_pymunk_space():
    '''returns a `space` where the physics happens'''
    space = pymunk.Space()
    # gravity is represented by a tuple 
    # 0 acceleration in x-axis and -9.8 in y-axis
    space.gravity = (0,-90.8)
    return space

# game width and height
GW = 800
GH = 800
# must be global because the @decorators work that way
window = pyglet.window.Window(GW, GH, __file__, resizable=False)
space = get_pymunk_space()
options = DrawOptions() 

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

def get_pymunk_rigid_poly():
    '''
    returns a `rigid body` which is a shapeless object that 
    has physical properties (mass, position, rotation, velocity, etc)
    ALSO returns a Poly which is the Shape that really gets drawn
    '''
    mass = 1
    moment_of_inertia = 1666
    body_type = pymunk.Body.DYNAMIC
    body = pymunk.Body(mass, moment_of_inertia, body_type)
    x = 500
    y = 500
    body.position = (x, y)
    poly = pymunk.Poly.create_box(body)
    return body, poly

@window.event
def on_draw():
    '''
    stuff that happens when pyglet is drawing
    '''
    window.clear() # start with a clean window
    space.debug_draw(options)

def main():
    # make sure window and space are a thing
    assert window
    assert space

    body, poly = get_pymunk_rigid_poly()
 
    space.add(body, poly)

    # do the update on 1/60th clock-ticks
    update = lambda dt: space.step(dt)
    schedule(update)

    run()

if __name__ == "__main__":
    print("hello world")
    main()
