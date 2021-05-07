#!/bin/env python3
# This script will take an svg file and output its path in a format
# that draw_bezier can read.

from sys import argv


def get_nums():
    if len(argv) == 1:
        text = input("Pasted the contents inside of the d attribute of path: ")

    else:
        # Read the contents of the file
        with open(argv[1], 'r') as file:
            text = file.readlines()

        text = ' '.join(text)

    values = text.split()

    # Quick checks to see if the file is in the correct format
    check = 0
    if values[0] == 'm':
        del values[0]
        check += 1

    if values[-1] == 'z':
        del values[-1]
        check += 1

    if values[1] == 'c':
        del values[1]
        check += 1

    letters = 0
    for item in values:
        if item.isalpha():
            letters += 1

    if letters or check != 3:
        raise Exception('Format must be composed of only relative cubic bezier curves')

    return values


def svg_str_to_tuple(str_list):
    """
    Turns the list of svg coords into tuples instead of strings
    :param str_list:
    :return:
    """
    new_list = []
    for item in str_list:
        new_list.append(eval("({})".format(item)))

    return new_list


def make_sections(ls, size, spaces=None):
    """
    splits list with sections of determined size
    fills in with spaces if keyword is given
    """
    new_list = []

    # Remove from list
    while len(ls) >= size:
        new_list.append(ls[:size])
        del ls[:size]

    # Check if there are any leftovers
    if len(ls):
        if spaces != None:
            # Add amount of spaces needed to fulfill size
            for i in range(size - len(ls)):
                ls.append(spaces)
        # Add leftovers
        new_list.append(ls)

    return new_list


def convert_to_absolute(first, points):
    """
    Converts a list of relative coordinates for a cubic
    bezier curve into absolute coordinates
    """
    coords = []
    prev = first
    for point in points:
        # Point will look like [(x,y), (x,y), (x,y)]
        # Starting point
        new_points = [prev]

        # Add the value of the previous point to the coordinates
        new_points += [(coord[0] + prev[0], coord[1] + prev[1]) for coord in point]

        coords.append(new_points)

        prev = new_points[-1]

    return coords


def main():
    txt_list = get_nums()
    coord_list = svg_str_to_tuple(txt_list)

    if not len(coord_list) - 1 % 3:
        # If the lenght of the list -1 isnt a multiple of three:
        raise Exception('Make sure the input is a relative cubic bezier')

    first_coord, *rest = coord_list

    # Split the list into sections of three
    extra_coords = make_sections(rest.copy(), 3)

    bezier_coords = convert_to_absolute(first_coord, extra_coords)

    print()
    print(bezier_coords)

if __name__ == "__main__":
    main()