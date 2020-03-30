import pygame
from pygame import *
from laws_motions import *
import math as mt

WIN_WIDTH = 800
WIN_HEIGHT = 640
PLANET_WIDTH = 20
PLANET_HEIGHT = 20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
SPACE_COLOR = "white"
SUN_COLOR = "red"
PLANET_COLOR = "blue"


# координаты солнца
X0 = WIN_WIDTH // 2
Y0 = WIN_HEIGHT // 2

# большая полуось
a = 149

# эксцентриситет
ec = 0.8

# средняя угловая скорость
T = 150

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Solar Mechanics v0.1")

    # background
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(SPACE_COLOR))
    draw.circle(bg, Color(SUN_COLOR), (X0, Y0), 10)

    timer = pygame.time.Clock()

    planet = Surface((PLANET_WIDTH, PLANET_HEIGHT))
    planet.fill(Color(SPACE_COLOR))
    law = EllipticalKeplersMotion(T, 150, 0.76)

    draw.circle(planet,
                Color(PLANET_COLOR),
                (PLANET_WIDTH // 2, PLANET_HEIGHT // 2),
                5)

    # координаты планеты
    x = 0
    y = 0

    done = False
    time_ = 0
    while not done:
        timer.tick(30)

        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
                break

        r = law.r(time_)
        f = law.rotation(time_)

        if time_ <= T:
            x = X0 + r * mt.cos(f)
            y = Y0 - r * mt.sin(f)

        time_ += 1
        screen.blit(bg, (0, 0))
        screen.blit(planet, (int(x), int(y)))
        pygame.display.update()


if __name__ == "__main__":
    main()
