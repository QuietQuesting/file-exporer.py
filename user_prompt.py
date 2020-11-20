# user_prompts.py
"""Input functions for file_explorer.py"""

import os
import output
from typing import Union


class GetNum:
    default_num = 0
    default_range = (1, 10)  # range includes 0 and 10

    def __init__(self, number_range=None, number=None):
        """ Prompts user to input a number within num_range()"""
        self.num_range = number_range
        self.num = number

        if not self.num_range_okay():
            self.num_range = GetNum.default_range

        if not self.num_okay():
            self.num = GetNum.default_num

    def in_range(self):
        while not self.condition():

            self.num = input('Enter your number now: ')
            try:
                self.num = int(self.num)
                if not self.condition():
                    print('Number out of range! Input number within 1 - {}.'.format(self.num_range[1]))

            except TypeError:
                print("Not a num.")

        return self.num

    def num_okay(self) -> bool:
        """Checks if num is okay. Value not important gets fixed later."""
        if not isinstance(self.num, int):
            return False
        return True

    def num_range_okay(self) -> bool:
        if isinstance(self.num_range, tuple) and len(self.num_range) == 2:
            for item in self.num_range:
                if not isinstance(item, int):
                    return False

            if self.num_range[0] < self.num_range[1]:
                return True

        return False

    def condition(self) -> bool:
        return self.num_range[0] <= self.num <= self.num_range[1]


def input_folder_num(number: int = 0) -> int:
    """ Accepts numbers within range of cwd.
    Special nums: 0 counts as abort. -1 as confirm."""
    if not isinstance(number, int):
        number = 0
    folder_range = (1, len(os.listdir(os.getcwd())))

    return GetNum(folder_range, number).in_range()


def input_amount(min_num: int = 1) -> int:
    """Prompts user to input a number equal or bigger than min_num.
    Defaults min_num to 1 in case it's not an int or a negative int."""
    if not isinstance(min_num, int) or min_num < 1:
        min_num = 1

    amount_range = (min_num, 100)

    print("How many files or folders?")

    return GetNum(amount_range).in_range()


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
                os.chdir('..\\')  # change to parent dir
                output.print_dir('..\\')  # parent dir
                print("Going to parent folder.")

            else:   # open folder / ask if user wants to select this file
                dir_list = os.listdir(os.getcwd())
                file_name = dir_list[num-1]  # file or folder
                f_path = os.getcwd() + '\\' + file_name

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
