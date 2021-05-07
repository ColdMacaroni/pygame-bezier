#!/bin/env python3
# Draw bezier curves
#
import math
import time

import pygame


def xy(x, y):
    """
    A shortcut to center_coords and py_coords.
    """
    return py_coords(center_coords((x, y)))


def un_xy(x, y):
    """
    does the opposite of xy
    """
    return un_center_coords(py_coords((x, y)))


def center_coords(coords, plane=None):
    """
    Repositions coords to the centre of the given plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return width/2 + coords[0], height/2 + coords[1]


def un_center_coords(coords, plane=None):
    """
    Repositions coords to the bottom left of the plane
    """
    if plane is None:
        width, height = screen_size()
    else:
        width, height = plane[0], plane[1]

    return coords[0] - width/2, coords[1] - height/2


def py_coords(coords):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    height = screen_size()[1]
    return coords[0], height - coords[1]


def un_py_coords(coords):
    """Convert coordinates into cardinal coordinates (top-left => lower left)."""
    height = screen_size()[1]
    return coords[0], height + coords[1]


def screen_size():
    """
    Set screen size
    """
    return 600, 600


def linear_interpolation(low, big, t):
    return ((low - big) * t) + low


def cubic_bezier(p0, p1, p2, p3, t):
    """
    Returns the point
    """
    coords = []
    # twice for x and then y
    for i in [0, 1]:
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Cubic_B%C3%A9zier_curves
        num = (((1 - t)**3) * p0[i])\
             + (3 * t * ((1 - t)**2) * p1[i])\
             + (3 * (t**2) * (1 - t) * p2[i])\
             + ((t**3) * p3[i])

        coords.append(num)

    return tuple(coords)


def draw_dot(screen, coord, color, size):
    pygame.draw.circle(screen, color, coord, size)


def main():
    pygame.init()

    size = width, height = screen_size()

    color = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'light_gray': (100, 100, 100),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    raw_points = [[(67.604009, 83.979588), (71.96352800000001, 46.407509000000005), (92.55386800000001, 83.600739), (99.074368, 83.600739)], [(99.074368, 83.600739), (105.59487, 83.600739), (115.51908, 57.304534000000004), (123.34958, 84.431239)], [(123.34958, 84.431239), (131.18009, 111.55795), (102.7013, 117.89734000000001), (96.675746, 101.04878000000001)], [(96.675746, 101.04878000000001), (90.650191, 84.20021000000001), (89.347407, 114.83774000000001), (76.915239, 112.31258000000001)], [(76.915239, 112.31258000000001), (64.48307199999999, 109.78742000000001), (67.604009, 83.979588), (67.604009, 83.979588)]]

    # Make em big
    factor = 2
    norm_points = []
    for point in raw_points:
        norm_points.append([(y[0] * factor, y[1] * -factor) for y in point])

    dots = []

    increment = 0.05

    # So the t=0 point is draw
    t = -increment
    while 1:
        t += increment

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        screen.fill(color['white'])

        # X
        pygame.draw.line(screen, color['light_gray'], xy(-width / 2, 0), xy(width / 2, 0))
        # Y
        pygame.draw.line(screen, color['light_gray'], xy(0, height / 2), xy(0, -height / 2))

        # Calculate position
        for points in norm_points:
            new_dot = tuple(map(lambda x: round(x, 2), cubic_bezier(*points, t)))

            if new_dot not in dots:
                dots.append(new_dot)

        prev = dots[0]
        for dot in dots:
            draw_dot(screen, xy(*dot), color['blue'], 1)

            # pygame.draw.line(screen, color['green'], xy(*prev), xy(*dot), 1)

            prev = dot

        if t > 1:
            t = 0

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
