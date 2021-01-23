# user_prompts.py
"""Input functions for file_explorer.py"""

import os

from output import print_help
import item_operations
import easy_multiple_select


def input_folder_num(number: int = -1) -> tuple:
    """ Accepts numbers within range of cwd.
    Returns -1 if number is abort"""
    dir_list = os.listdir(os.getcwd())

    if not isinstance(number, int):
        number = -1  # tuple

    while not -1 < number <= len(dir_list):

        number = input('Enter your number now: ')

        if not number.isdecimal():

            if number == '':
                return (-1, )  # tuple

            elif easy_multiple_select.is_multiple_select(number, len(dir_list)):
                return easy_multiple_select.run_multiple_select(number)

            else:
                print('That is not a number nor a valid command.')
                number = -1

        else:
            number = int(number)
            if not -1 < number <= len(dir_list):
                print('Number out of range! Input number between 1 - {}.'.format(len(dir_list)))

    return (number, )  # tuple


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


class Options:
    def __init__(self):
        self.clipboard = {"copy": [], "move": []}

    def copy(self, items):
        """Extends item list in copy list"""
        self.clipboard["copy"].extend(items)

    def move(self, items):
        """Extends item list in copy list"""
        self.clipboard["move"].extend(items)

    def paste(self, destination):
        """pastes all saved items to the destination and clears """
        if self.clipboard["copy"]:
            item_operations.Copy(self.remove_duplicates(self.clipboard["copy"]), destination)

        if self.clipboard["move"]:
            item_operations.Move(self.remove_duplicates(self.clipboard["move"]), destination)

        self.clear_clipboard()

    def clear_clipboard(self):
        self.clipboard["copy"] = []
        self.clipboard["move"] = []

    @staticmethod
    def remove_duplicates(x: list) -> list:
        return list(dict.fromkeys(x))

    def select(self, paths):
        """
        Select option of what to do with the file and run the associated function/class

        :param: paths as a path
        """
        paths = self.remove_duplicates(paths)
        option = input("Please choose an option for the item: ").lower()

        while True:

            if option == "o":
                print('Option: open item\\s')
                item_operations.Open(paths)
                break

            elif option == 'c':
                print('Option: copy item\\s\n')
                self.copy(paths)
                break

            elif option == 'm':
                print('Option: move item\\s\n')
                self.move(paths)
                break

            elif option == 'p':
                print('Option: paste item\\s \n')
                if not len(paths) > 1:
                    self.paste(paths[0])
                else:
                    print("Can't paste to multiple places.")
                break

            elif option == 'd':
                print('Option: delete item\\s\n')
                item_operations.Delete(paths)

            elif option == 'nf':
                print('Option: create new file in directory\\s\n')
                item_operations.Create(paths, "folder")
                break

            elif option == 'nd':
                print('Option: create new subdirectory\\s\n')
                item_operations.Create(paths, "sub directory")
                break

            elif option == 's':
                print('Option: search item\\s\n')
                break

            elif option == 'e':
                print("Option: exit option selection\n")
                break

            elif option == 'h':
                print('Option: print help\n')
                print_help()
                option = input("Please choose an option for the item: ").lower()
                # no break statement to let the user choose an option without re-selecting the item\s.

            else:
                print("Unknown command. Enter option (h) to get list of commands (e) for exit option selecting.")
                option = input("Please choose an option for the item: ").lower()


