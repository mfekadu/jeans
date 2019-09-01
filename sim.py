#!/usr/bin/env python3

import pyglet  # for displaying to screen
import pymunk  # for rigid body physics
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction


def get_pymunk_space():
    '''returns a `space` where the physics happens'''
    space = pymunk.Space()
    # gravity is represented by a tuple
    # 0 acceleration in x-axis and -9.8 in y-axis
    space.gravity = (0, -90.8)
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


def get_pentagon():
    mass = 1
    # vertices are defined counter-clockwise from bottom-left (origin)
    penta_vertices = ((0, 0), (100, 0), (150, 100), (50, 200), (-50,  100))
    penta_shape = pymunk.Poly(body=None, vertices=penta_vertices)
    penta_vertices = penta_shape.get_vertices()
    penta_moment = pymunk.moment_for_poly(mass=mass, vertices=penta_vertices)
    penta_body = pymunk.Body(mass=mass, moment=penta_moment)
    penta_body.position = (700, 800)
    penta_shape.body = penta_body
    return penta_body, penta_shape


def get_triangle():
    '''
    return a triangle
    '''
    mass = 1
    triangle_vertices = ((0, 0), (100, 0), (50, 100))  # equilateral
    triangle_shape = pymunk.Poly(body=None, vertices=triangle_vertices)
    triangle_vertices = triangle_shape.get_vertices()  # because Vec2d
    triangle_moment = pymunk.moment_for_poly(mass=mass,
                                             vertices=triangle_vertices)
    triangle_body = pymunk.Body(mass=mass, moment=triangle_moment)
    triangle_body.position = (550, 700)
    triangle_shape.body = triangle_body  # set here because init None above
    return triangle_body, triangle_shape


def get_segment():
    '''
    return a line segment
    '''
    point_1 = (0, 0)
    point_2 = (0, 400)
    mass = 1
    thiccness = 2
    seg_mom = pymunk.moment_for_segment(mass=mass,
                                        a=point_1,
                                        b=point_2,
                                        radius=thiccness)
    seg_body = pymunk.Body(mass=mass, moment=seg_mom)
    seg_shape = pymunk.Segment(body=seg_body,
                               a=point_1,
                               b=point_2,
                               radius=thiccness)
    seg_body.position = (400, 100)
    return seg_body, seg_shape


def get_pymunk_rigid_circle():
    mass = 1
    radius = 70
    circle_moment = pymunk.moment_for_circle(mass=mass,
                                             inner_radius=0,
                                             outer_radius=radius)
    circle_body = pymunk.Body(mass=mass, moment=circle_moment)
    circle_shape = pymunk.Circle(body=circle_body, radius=radius)
    circle_body.position = (400, 400)
    return circle_body, circle_shape


def get_pymunk_rigid_poly():
    '''
    returns a `rigid body` which is a shapeless object that
    has physical properties (mass, position, rotation, velocity, etc)
    ALSO returns a Poly which is the Shape that really gets drawn
    '''
    mass = 1
    body_type = pymunk.Body.DYNAMIC

    poly_size = (150, 150)
    poly = pymunk.Poly.create_box(body=None, size=poly_size)
    # moment depends on mass and size.
    # bigger poly >> bigger moment.
    # more massive >> bigger moment
    moment_of_inertia = pymunk.moment_for_poly(mass, poly.get_vertices())

    body = pymunk.Body(mass, moment_of_inertia, body_type)
    x = 500
    y = 500
    body.position = (x, y)

    poly.body = body
    return body, poly


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

    body, poly = get_pymunk_rigid_poly()

    space.add(body, poly)

    cbody, cshape = get_pymunk_rigid_circle()
    space.add(cbody, cshape)

    line_body, line_shape = get_segment()
    space.add(line_body, line_shape)

    tbody, tshape = get_triangle()
    space.add(tbody, tshape)

    pb, ps = get_pentagon()
    space.add(pb, ps)

    # do the update on 1/60th clock-ticks
    def update(dt): return space.step(dt)
    schedule(update)

    run()


if __name__ == "__main__":
    print("hello world")
    main()
