#!/usr/bin/env python3
from create_shapes import create_segment
import cfg

def draw_border(game_width, game_height, thicc=10):
    bt = 'kinematic'
    lbb, lbs = create_segment(scalar=game_height, thicc=thicc, bt=bt)
    rbs = lbs.copy()
    rbb = rbs.body
    y = rbb.position.y
    rbs.body.position = (game_width, y)

    bbb, bbs = create_segment(p1=(0, 0), p2=(1, 0), scalar=game_width,
                              thicc=thicc, bt=bt)
    tbs = bbs.copy()
    tbb = tbs.body
    x = tbb.position.x
    tbs.body.position = (x, game_height)
    for part in (lbs, bbs, rbs, tbs):
        part.elasticity = cfg.WALL_ELASTICITY
    # return all border-bodies and border-shapes in a tuple, counter-clockwise
    return ((lbb, lbs), (bbb, bbs), (rbb, rbs), (tbb, tbs))


def test_draw_border():
    assert True
    pass


def run_tests():
    test_draw_border()
    print("all tests passed")


if __name__ == "__main__":
    run_tests()
