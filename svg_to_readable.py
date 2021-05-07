#!/bin/env python3
# This script will take an svg file and output its path in a format
# that draw_bezier can read.

def get_nums():
    text = input("Pasted the contents inside of the d attribute of path: ")

    values = text.split()

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

    print(values)

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


def main():
    print(1)
    txt_list = get_nums()
    coord_list = svg_str_to_tuple(txt_list)

    # Split the list into sections of 3, expect for the first which will be of 4.
    # then on each section of 3 insert at the start the last item of the last section
    # Add the coordinates of the last item to the other 3 in the section
    # Rinse and repeat
    # Should be enough for the other .py to work


if __name__ == "__main__":
    main()