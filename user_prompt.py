# user_prompts.py
"""Input functions for file_explorer.py"""

import os
import output
from typing import Union


def input_folder_num(number: int = -1) -> int:
    """ Accepts numbers within range of cwd.
    Special nums: 0 counts as abort. -1 as confirm."""
    dir_list = os.listdir(os.getcwd())

    if not isinstance(number, int):
        number = -1

    while not -1 < number <= len(dir_list):

        number = input('Enter your number now: ')

        if not number.isdecimal():

            if number == '':
                return -1

            elif number in ('..', '.'):
                return -2

            else:
                print('That is not a number nor a valid command.')
                number = -1

        else:
            if not -1 < int(number) <= len(dir_list):
                print('Number out of range! Input number between 1 - {}.'.format(len(dir_list)))

    return number


def input_amount(min_num: int = 1) -> int:
    """Prompts user to input a number equal or bigger than min_num.
    Defaults min_num to 1 in case it's not an int or a negative int."""
    if not isinstance(min_num, int) or min_num < 1:
        min_num = 1

    number = input("How many files or folders?")
    while True:
        try:
            number = int(input("Please input a number bigger than {}.".format(min_num)))

        except ValueError:
            pass

        if min_num <= int(number):
            break

    return number


def select(count: int = 1) -> Union[list[str], bool]:
    """Prompt user to select file or folder."""
    print('Please input a number to open the associated folder or select the file.',
          'Else input 0 to cancel and enter to choose the current folder.',
          'Else enter ".." to go back up', sep='\n')

    if not isinstance(count, int) or count < 1:
        count = 1

    selection = []

    print('Please select {} folder or files, one after the other'.format(count))
    for _ in range(count):

        selected = False

        while not selected:
            num = input_folder_num()

            if num == 0:
                print('Aborting process.')
                return False

            elif num == -1:
                print('Current folder is selected!')
                selection.append(os.getcwd())
                selected = True

            elif num == -2:
                os.chdir('../')  # change to parent dir
                output.print_dir('../')  # parent dir
                print("Going to parent folder.")

            else:   # open folder / ask if user wants to select this file
                dir_list = os.listdir(os.getcwd())
                file_name = dir_list[num-1]  # file or folder
                f_path = os.getcwd() + '/' + file_name

                if os.path.isfile(f_path):
                    choice = input('Do you want to select {}? (y, yes)'.format(file_name))

                    if choice.replace(' ', '').lower() in ('y', 'yes'):
                        print('File selected!')
                        selection.append(f_path)
                        selected = True

                    else:
                        print('File not selected.\n')
                else:
                    os.chdir(f_path)
                    print('Going into selected folder: '.format(f_path))
                    output.print_dir(f_path)
    return selection
