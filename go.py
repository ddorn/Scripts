"""
This script is intended to travel easily in my computer.
It is a pair with go.bat, which is indispensable for this script to run.
"""

import os
import click
import readline
from debugging import *

DIR = os.path.abspath(os.path.dirname(__file__))
FILE = os.path.join(DIR, 'locations.txt')
OUTFILE = os.path.join(DIR, 'temp.txt')

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
        mapping[shortcut] = path

    save_mapping(mapping)

def save_mapping(mapping: dict):
    """Save a mapping of shortcuts and paths."""

    # we sort the items by alphabetical order of path    
    pairs = list(mapping.items())
    pairs.sort(key=lambda x: (x[1]))

    with open(FILE, 'w') as file:
        for shortcut, path in pairs:
            file.write(f'{shortcut} {path}\n')

def correct(to, locations):
    import difflib
    possible = list(set(list(locations.keys()) + next(os.walk('.'))[1]))
    possible = difflib.get_close_matches(to, possible)

    if not possible:
        return

    print('Do you mean ', end='')
    for loc, sep in zip(possible, [', ', ', ', ' or ', ''][-len(possible):]):
        blue(loc, end=sep)
    print(' ?')
    to = prompt_choice('path', possible, 0)
    try:
        return locations[to]
    except KeyError:
        return to

def prompt_choice(prompt, choices, default: int = None):
    """
    Prompt a text name with autocompletion.

    Choices is a list of possible texts.
    Default is the index of the default possibility
    """

    def complete(text: str, state):
        return ([c for c in choices if c.startswith(text)] + [None,])[state]

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    good = False
    while not good:
        if default is not None:
            r = input('%s [%r]: ' % (prompt, choices[default]))
        else:
            r = input('%s: ' % prompt)

        if default is not None:
            r = r or choices[default]

        if r in choices:
            good = True
        else:
            print("%s is not a valid choice." % r)

    # remove the autocompletion before quitting for future input()
    readline.parse_and_bind('tab: self-insert')

    return r


@click.command()
@click.argument('to', required=False)
@click.argument('add-location', default=None, required=False)
@click.option('--out-dir-file', default=OUTFILE, help='The file to print the path to go')
@click.option('--delete', '-d', is_flag=True)
def go(to: str = None, add_location: str = None, out_dir_file: str=None, delete: bool=False):
    """Go somewhere !"""

    locations = load_mapping()

    # we want to remove a shortcut
    if delete:
        try:
            del locations[to]
            save_mapping(locations)
            print('The shortcut ', end='')
            blue(to, end=' ')
            print('was deleted.')
        except KeyError:
            red('No such shortcut to delete (%s)' % to)
        return

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
        if os.path.exists(to):
            path = to
        else:
            path = correct(to, locations)
            if not path:
                red('Can not find any correspondance...')
                return

    with open(out_dir_file, 'w') as outtempfile:
        print(path, file=outtempfile)


if __name__ == '__main__':
    go()