#!/usr/bin/env python3
# get_d_svg.py
# A script to get the d attribute of a path element in an svg
# This is used to pass to svg_to_readable.py

from sys import argv
import bs4 as bs


def main():
    source = open(argv[1], 'r')

    soup = bs.BeautifulSoup(source, 'xml')

    path = soup.find('path')

    # TODO: Add support for multiple paths
    if path is list:
        path = path[0]


if __name__ == "__main__":
    main()
