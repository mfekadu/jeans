#!/usr/bin/env python3

import pyglet  # for displaying to screen
import pymunk  # for rigid body physics
from pymunk.pyglet_util import DrawOptions  # pymunk/pyglet interaction


def get_pymunk_space():
    '''returns a `space` where the physics happens'''
    space = pymunk.Space()
    # gravity is represented by a tuple
    # 0 acceleration in x-axis and -9.8 in y-axis
    space.gravity = (0, -9.807)
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


def create_pentagon(p1=(0, 0), p2=(2, 0), p3=(3, 2), p4=(1, 4), p5=(-1, 2),
                    x=0, y=0, m=1, scalar=1, bt=pymunk.Body.DYNAMIC):
    '''
    given points (p1..p5), mass (m), x-position (x), y-position (y),
          scalar <to augment default points>, body_type (bt),
    return (body, shape) tuple for a pentagon
    '''
    vertices = (p1, p2, p3, p4, p5)
    vertices = tuple((v[0]*scalar, v[1]*scalar) for v in vertices)
    shape = pymunk.Poly(body=None, vertices=vertices)  # will set body later
    vertices = shape.get_vertices()  # because Vec2d of vertices is needed
    moment = pymunk.moment_for_poly(mass=m, vertices=vertices)
    body = pymunk.Body(mass=m, moment=moment)
    body.position = (x, y)
    shape.body = body  # set body here because init None above
    return body, shape


def create_triangle(p1=(0, 0), p2=(1, 0), p3=(.5, .866), x=0, y=0,
                    m=1, scalar=1, bt=pymunk.Body.DYNAMIC):
    '''
    given points (p1..p3), mass (m), x-position (x), y-position (y),
          scalar <to augment default equilateral triangle>, body_type (bt),
    The default values for p1,p2,p3 make an approx. equilateral triangle.
    return (body, shape) tuple for a triangle
    '''
    vertices = (p1, p2, p3)  # equilateral
    vertices = tuple((v[0]*scalar, v[1]*scalar) for v in vertices)
    shape = pymunk.Poly(body=None, vertices=vertices)  # will set body later
    vertices = shape.get_vertices()  # because Vec2d of vertices is needed
    moment = pymunk.moment_for_poly(mass=m, vertices=vertices)
    body = pymunk.Body(mass=m, moment=moment)
    body.position = (x, y)
    shape.body = body  # set body here because init None above
    return body, shape


def create_segment(p1=(0, 0), p2=(0, 1), thicc=1, x=0, y=0, m=1, scalar=1,
                   bt=pymunk.Body.DYNAMIC):
    '''
    given point_1 (p1), point_2 (p2), thickness (thicc),
          x-position (x), y-position (y), mass (m),
          scalar <to augment the length>, body_type (bt)
    return (body, shape) tuple for a line segment
    '''
    p2 = (p2[0], p2[1]*scalar)
    moment = pymunk.moment_for_segment(mass=m, a=p1, b=p2, radius=thicc)
    body = pymunk.Body(mass=m, moment=moment, body_type=bt)
    shape = pymunk.Segment(body=body, a=p1, b=p2, radius=thicc)
    body.position = (x, y)
    return body, shape


def create_circle(r=1, x=0, y=0, m=1, bt=pymunk.Body.DYNAMIC):
    '''
    given radius (r), x-position (x), y-position (y), mass (m), body_type (bt)
    return the (body, shape) tuple for a circle
    '''
    moment = pymunk.moment_for_circle(mass=m, inner_radius=0, outer_radius=r)
    body = pymunk.Body(mass=m, moment=moment)
    shape = pymunk.Circle(body=body, radius=r)
    body.position = (x, y)
    return body, shape


def create_rect(w=1, h=1, scalar=1, m=1, x=0, y=0, bt=pymunk.Body.DYNAMIC):
    '''
    given the width (w), height (h), mass (m), x-position (x), y-position (y),
        scalar <to augment default square>, and the body_type (bt).
    returns a `rigid body` which is a shapeless object that
    has physical properties (mass, position, rotation, velocity, etc)
    ALSO returns a Poly which is the Shape that really gets drawn
    '''
    poly_size = (w*scalar, h*scalar)
    poly = pymunk.Poly.create_box(body=None, size=poly_size)
    # moment depends on mass and size.
    # bigger poly >> bigger moment.
    # more massive >> bigger moment
    moment_of_inertia = pymunk.moment_for_poly(m, poly.get_vertices())
    body = pymunk.Body(mass=m, moment=moment_of_inertia, body_type=bt)
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

    body, poly = create_rect(x=300, y=300, scalar=50)

    space.add(body, poly)

    cbody, cshape = create_circle(r=50, x=400, y=400)
    space.add(cbody, cshape)

    line_body, line_shape = create_segment(x=600, y=600, scalar=50)
    space.add(line_body, line_shape)

    tbody, tshape = create_triangle(x=100, y=600, scalar=50)
    space.add(tbody, tshape)

    pb, ps = create_pentagon(x=150, y=150, scalar=50)
    space.add(pb, ps)

    # do the update on 1/60th clock-ticks
    def update(dt): return space.step(dt)
    schedule(update)

    run()


if __name__ == "__main__":
    print("hello world")
    main()
