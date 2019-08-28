#!/usr/bin/env python3

import pygame

# game width and height
GW = 800
GH = 800

def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((GW, GH))
    CLOCK = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    #quit()

if __name__ == "__main__":
    print("hello world")
    main()
