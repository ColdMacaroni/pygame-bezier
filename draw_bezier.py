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

    raw_points = [[(0, 0), (4.68822, -9.06797), (-2.60655, -10.18185), (-0.86152, -14.39585)], [(-0.86152, -14.39585), (0.8835100000000001, -18.609859999999998), (8.46781, -15.32504), (10.4117, -25.99175)], [(10.4117, -25.99175), (11.38365, -31.32511), (-1.7129100000000008, -33.283), (-6.197120000000002, -33.69267)], [(-6.197120000000002, -33.69267), (-8.024570000000002, -33.72337), (-1.3975600000000021, -41.27619), (-3.4131400000000016, -41.8501)], [(-3.4131400000000016, -41.8501), (-5.391580000000001, -42.413439999999994), (-8.796000000000001, -33.98813), (-9.790690000000001, -34.42445)], [(-9.790690000000001, -34.42445), (-11.541890000000002, -35.19261), (-8.633310000000002, -44.75384), (-11.418510000000001, -44.5681)], [(-11.418510000000001, -44.5681), (-14.203710000000001, -44.38237), (-10.0447, -34.64056), (-13.802760000000001, -35.66668)], [(-13.802760000000001, -35.66668), (-17.07917, -36.53915), (-21.80949, -48.9543), (-31.314968, -44.86435)], [(-31.314968, -44.86435), (-40.820442, -40.77441), (-30.980815, -26.08339), (-33.413413, -22.514460000000003)], [(-33.413413, -22.514460000000003), (-35.846016, -18.945530000000005), (-46.755883999999995, -19.800270000000005), (-42.848062, -7.631140000000004)], [(-42.848062, -7.631140000000004), (-38.940239999999996, 4.537989999999995), (-22.777549999999998, -8.283880000000003), (-18.48756, -5.400100000000004)], [(-18.48756, -5.400100000000004), (-14.197569999999999, -2.516320000000004), (-5.773999999999999, 9.133679999999996), (0.0, 2.9999999996199733e-05)]]

    # Make em big
    factor = 2
    norm_points = []
    for point in raw_points:
        # The y has to be flipped for the image to look the same
        norm_points.append([(y[0] * factor, y[1] * -factor) for y in point])

    dots = []

    increment = 0.1|

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

            else:
                print(dots)
                input()

        prev = dots[0]
        for dot in dots:
            draw_dot(screen, xy(*dot), color['blue'], 1)

            # Doesnt work as intended.
            # pygame.draw.line(screen, color['green'], xy(*prev), xy(*dot), 1)

            prev = dot

        if t > 1:
            t = 0

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
