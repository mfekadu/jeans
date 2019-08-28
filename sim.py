#!/usr/bin/env python3

import pygame # for displaying to screen
import pymunk # for rigid body physics
from pymunk.pygame_util import DrawOptions
import time

# game width and height
GW = 800
GH = 800

def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((GW, GH))
    CLOCK = pygame.time.Clock()
    def draw():
        pass

    def update():
        CLOCK.tick()


    space = pymunk.Space()
    space.gravity = 0, -1
    body = pymunk.Body(1, 1666)
    body.position = 640, 700
    poly = pymunk.Poly.create_box(body, size=(50,50))
    surface = pygame.Surface((10,10))
    options = DrawOptions(surface)
#    space.add(body)

#    space.add(body, poly)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        space.step(0.02) # 1/50
        print(body.position)

        space.debug_draw(options)
#        draw()
#        update()

    pygame.quit()
    #quit()

if __name__ == "__main__":
    print("hello world")
    main()
