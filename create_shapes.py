#!/usr/bin/env python3

from pymunk import Poly, Body, Segment, Circle
from pymunk import moment_for_poly, moment_for_segment, moment_for_circle


def create_pentagon(p1=(0, 0), p2=(2, 0), p3=(3, 2), p4=(1, 4), p5=(-1, 2),
                    x=0, y=0, m=1, scalar=1, bt=Body.DYNAMIC):
    '''
    given points (p1..p5), mass (m), x-position (x), y-position (y),
          scalar <to augment default points>, body_type (bt),
    return (body, shape) tuple for a pentagon
    '''
    vertices = (p1, p2, p3, p4, p5)
    vertices = tuple((v[0]*scalar, v[1]*scalar) for v in vertices)
    shape = Poly(body=None, vertices=vertices)  # will set body later
    vertices = shape.get_vertices()  # because Vec2d of vertices is needed
    moment = moment_for_poly(mass=m, vertices=vertices)
    body = Body(mass=m, moment=moment)
    body.position = (x, y)
    shape.body = body  # set body here because init None above
    return body, shape


def create_triangle(p1=(0, 0), p2=(1, 0), p3=(.5, .866), x=0, y=0,
                    m=1, scalar=1, bt=Body.DYNAMIC):
    '''
    given points (p1..p3), mass (m), x-position (x), y-position (y),
          scalar <to augment default equilateral triangle>, body_type (bt),
    The default values for p1,p2,p3 make an approx. equilateral triangle.
    return (body, shape) tuple for a triangle
    '''
    vertices = (p1, p2, p3)  # equilateral
    vertices = tuple((v[0]*scalar, v[1]*scalar) for v in vertices)
    shape = Poly(body=None, vertices=vertices)  # will set body later
    vertices = shape.get_vertices()  # because Vec2d of vertices is needed
    moment = moment_for_poly(mass=m, vertices=vertices)
    body = Body(mass=m, moment=moment)
    body.position = (x, y)
    shape.body = body  # set body here because init None above
    return body, shape


def create_segment(p1=(0, 0), p2=(0, 1), thicc=1, x=0, y=0, m=1, scalar=1,
                   bt=Body.DYNAMIC):
    '''
    given point_1 (p1), point_2 (p2), thickness (thicc),
          x-position (x), y-position (y), mass (m),
          scalar <to augment the length>, body_type (bt)
    return (body, shape) tuple for a line segment
    '''
    p2 = (p2[0], p2[1]*scalar)
    moment = moment_for_segment(mass=m, a=p1, b=p2, radius=thicc)
    body = Body(mass=m, moment=moment, body_type=bt)
    shape = Segment(body=body, a=p1, b=p2, radius=thicc)
    body.position = (x, y)
    return body, shape


def create_circle(r=1, x=0, y=0, m=1, bt=Body.DYNAMIC):
    '''
    given radius (r), x-position (x), y-position (y), mass (m), body_type (bt)
    return the (body, shape) tuple for a circle
    '''
    moment = moment_for_circle(mass=m, inner_radius=0, outer_radius=r)
    body = Body(mass=m, moment=moment)
    shape = Circle(body=body, radius=r)
    body.position = (x, y)
    return body, shape


def create_rect(w=1, h=1, scalar=1, m=1, x=0, y=0, bt=Body.DYNAMIC):
    '''
    given the width (w), height (h), mass (m), x-position (x), y-position (y),
        scalar <to augment default square>, and the body_type (bt).
    returns a `rigid body` which is a shapeless object that
    has physical properties (mass, position, rotation, velocity, etc)
    ALSO returns a Poly which is the Shape that really gets drawn
    '''
    poly_size = (w*scalar, h*scalar)
    poly = Poly.create_box(body=None, size=poly_size)
    # moment depends on mass and size.
    # bigger poly >> bigger moment.
    # more massive >> bigger moment
    moment_of_inertia = moment_for_poly(m, poly.get_vertices())
    body = Body(mass=m, moment=moment_of_inertia, body_type=bt)
    body.position = (x, y)
    poly.body = body
    return body, poly


def test_create_rect():
    assert True
    pass


def test_create_circle():
    assert True
    pass


def test_create_segment():
    assert True
    pass


def test_create_triangle():
    assert True
    pass


def test_create_pentagon():
    assert True
    pass


def run_tests():
    test_create_rect()
    test_create_circle()
    test_create_segment()
    test_create_triangle()
    test_create_pentagon()


if __name__ == "__main__":
    run_tests()
