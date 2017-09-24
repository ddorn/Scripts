"""
This script is intended to travel easily in my computer.
It is a pair with go.bat, which is indispensable for this script to run.
"""

import os
import click
from debugging import *

DIR = os.path.abspath(os.path.dirname(__file__))
FILE = os.path.join(DIR, 'locations.txt')
OUTFILE = os.path.join(DIR, 'temp.txt')

def color(col, text):
    """Add the ansi esacape char aroud a string to print it colored"""
    return f'\033[0;3{col}m{text}\033[0m'


def load_mapping():
    """Get a dict with the shortcuts as key and the path the point to as value."""
    with open(FILE, 'r') as file:
        lines = file.readlines()

    locations = {}
    for line in lines:
        # we don't want the last \n
        line = line.rstrip()
        # parsing the line
        short, _, path = line.partition(' ')

        # no empty line nor no data ones
        if short and path:
            locations[short] = path

    return locations

def add_mapping(shortcut, path):
    """Add a shortcut and a path to the list."""
    if not os.path.exists(FILE):
        mapping = {shortcut: path}
    else:
        mapping = load_mapping()

    save_mapping(mapping)

def save_mapping(mapping: dict):
    """Save a mapping of shortcuts and paths."""

    # we sort the items by alphabetical order of path    
    pairs = list(mapping.items())
    pairs.sort(key=lambda x: (x[1]))

    with open(FILE, 'w') as file:
        for shortcut, path in pairs:
            file.write(f'{shortcut} {path}\n')

@click.command()
@click.argument('to', required=False)
@click.argument('add-location', default=None, required=False)
@click.option('--out-dir-file', default=OUTFILE, help='The file to print the path to go')
def go(to: str = None, add_location: str = None, out_dir_file: str=None):
    """Go somewhere !"""

    # we want to add a loc when a second param is specified
    if add_location:
        if ' ' in to:
            red('The shortcut can not contain any space')
        else:
            add_location = os.path.abspath(add_location)
            add_mapping(to, add_location)

            # tell it worked
            green('The mapping from ', end='')
            blue(to, end='')
            green(' to ', end='')
            blue(add_location, end='')
            green(' was succesfull.')
        return

    locations = load_mapping()

    # it was just 'go', so we show all the possible locations
    if not to:
        # we sort the items by alphabetical order of path
        pairs = list(locations.items())
        pairs.sort(key=lambda x: (x[1]))

        max_len = max(len(p[0]) for p in pairs)

        for key, path in pairs:
            arrow = '-' * (max_len - len(key) + 2) + '>'
            pink(key, end=' ')
            blue(arrow, end=' ')
            print(path)
        return

    # move to a new place
    try:
        path = locations[to]
    except KeyError:
        path = to

    with open(out_dir_file, 'w') as outtempfile:
        print(path, file=outtempfile)


if __name__ == '__main__':
    go()