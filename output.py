# output.py
"""Output functions for file_explorer.py"""

import os
import mimetypes


def print_intro() -> None:
    """ Simple introduction used at the start of main."""

    print('===========================',
          'Welcome to my file explorer!',
          '===========================',
          'Please choose one of the following options:\n', sep='\n')

    print_options(intro=True)
    print_dir(os.getcwd())
    return None


def print_options(intro: bool = False) -> None:
    """ Prints all current options user can use."""
    if not intro:
        print('\nYou can choose following options:\n')

    print('Enter number to open associated folder or file.',
          'Enter ".." to open parent folder.',
          'co / copy to copy file/folder',
          'm / move to crop file/folders',
          'del to move file/folders folders to paper bin',
          'or delete directly if not possible.', sep='\n')
    return None


def print_dir(folder: str) -> None:
    """Fancy prints directory and it's content."""
    intro = '\nContent of folder: {}'.format(folder)

    # get parent dir as a string
    last_slash = folder.rfind('\\')
    if last_slash == -1:
        last_slash = folder.rfind('/')

    if last_slash == -1:3
        raise OSError('Can\'t go back up!')

    parent_dir = folder[:last_slash]

    print(intro)
    print('o', len(intro) * '-', sep='')

    print(f'| ...\tparent folder:\t{parent_dir:30}')

    for index, item in enumerate(os.listdir(folder)):
        path = folder + '//' + item

        if item[-4:] == '.lnk':
            _type = 'link/shortcut'

        elif os.path.isfile(path):
            # Get Mimetype as tuple, want only first tuple item
            _type = mimetypes.guess_type(path, strict=False)[0]

            if _type is None:
                _type = 'unknown/uncommon'

        else:
            _type = 'dir/folder'

        print(f'| {index+1:02}.\t{item:20}{_type}')

    return None
