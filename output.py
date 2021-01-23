# output.py
"""Output functions for file_explorer.py"""

import os
from item_operations import get_mimetype
import pathlib


def print_intro() -> None:
    """ Simple introduction used at the start of main."""

    print('===========================',
          'Welcome to my file explorer!',
          '===========================',
          '\n', sep='\n')

    print('Enter number to open associated item. An item is either a file, folder, or a shortcut.',
          'You can also select multiple items, by doing an multiselect, eg.:',
          'enter 2-4 to get all items within the range (in this case 2,3,4) for separate items you can use comma',
          '2,4 will get you the values 2 and 4, you can also combine both ways like this 2-4, 6, leading to 2,3,4,6.',
          '\n', sep='\n')

    print('Then you can choose on of the following options for your item/s:')
    for item in option_list():
        print(item, sep='\n')

    print()
    print_dir()


def print_help() -> None:
    for item in option_list():
        print(item, sep=" - ")


def option_list() -> list:
    """Returns what user can do."""
    return [' (o) to open item', ' (c) to copy item', ' (m) to move item', ' (p) to paste selected item',
            ' (d) to delete item to to paper bin', ' (r) to rename item',
            '(nf) to create new folder', '(nd) to create new directory']


def print_dir(folder: str = os.getcwd()) -> None:
    """Fancy prints directory and it's content."""
    intro = f'\nContent of folder: {folder}'

    # get parent dir as a string
    folder = pathlib.Path(folder)
    parent_dir = folder.parent

    print(intro)
    print('o', len(intro) * '-', sep='')

    print(f'| 0 \tparent folder:\t{str(parent_dir):30}')

    for index, item in enumerate(os.listdir(folder)):
        path = folder / item  # thanks to pathlib

        mimetype = get_mimetype(path.name)

        print(f'| {index + 1:02}.\t{item:20}{mimetype}')

    return None


