# user_prompts.py
"""Input functions for file_explorer.py"""

import os
from typing import Union
import file_transport
import collection


def input_folder_num(number: int = -1) -> int:
    """ Accepts numbers within range of cwd.
    Returns -1 if number is abort"""
    dir_list = os.listdir(os.getcwd())

    if not isinstance(number, int):
        number = -1

    while not -1 < number <= len(dir_list):

        number = input('Enter your number now: ')

        if not number.isdecimal():

            if number == '':
                return -1

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


def select_option(file):
    """
    Select option of what to do with the file and run the associated function/class

    :param: file as a path
    """
    option = input("Please choose an option for the item: ").lower()

    while True:

        if option == "o":
            print('Option: open item')

            if file.isdir():
                collection.open_folder(file)

            else:
                collection.open_file()

            break

        elif option == "c":
            print('Option: copy item\n')
            break

        elif option == 'm':
            print('Option: move item\n')
            break

        elif option == 'p':
            print('Option: paste item\n')
            break

        elif option == 'd':
            print('Option: delete item\n')
            file_transport.Delete([file])

        elif option == 'nf':
            print('Option: create new file in directory\n')
            break

        elif option == 'nd':
            print('Option: create new subdirectory\n')
            break

        elif option == 's':
            print('Option: search item\n')
            break

        elif option == 'e':
            print("Option: exit option selection\n")
            break

        elif option == 'h':
            print('Option: print help\n')
            # no break statement to let the user choose an option without reselecting the file.

        else:
            print("Unknown command. Enter option (h) to get list of commands (e) for exit option selectin.")
