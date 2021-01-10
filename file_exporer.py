"""My own commandline file explorer module in python
    Planning to be used for:
        - bulk renaming of files
        - automatic file sorting routines
        
        Arguments:
1st: Optional path of config.ini"""


import sys
import os
import pathlib
from typing import Union
import configparser
import output
import user_prompt
import file_transport


def init_config(config_file='config.ini') -> str:
    """initializes configparser object with consideration of sys.argv"""
    config = configparser.ConfigParser()
    config.read(config_file)
        
    return config


def set_starting_dir(config):
    """ Looks for starting directory in config requires returned class from init_config
    Returns directory or else an empty string.
    Using $USERNAME in config doesn't work. os.getlogin() to get username executing the script"""
    # try:
    starting_dir = config['DEFAULT']['starting_dir']
    # print("Starting dir", starting_dir)

    # except:
    #     print("Default starting dir.")
    #     return False

    if not starting_dir or not os.path.isdir(starting_dir):
        return False

    os.chdir(starting_dir)


def main() -> None:
    """ Main script flow of the file explorer.
    In case you want to prompt the user to choose a folder/file use fselect. """
    config = init_config()
    set_starting_dir(config)
    output.print_intro()

    running = True
    while running:
        option = user_prompt.input_folder_num()

        if option != -1:

            directory = pathlib.Path(os.getcwd())

            # open parent and continue next loop
            if option == 0:
                user_prompt.select_option(directory.parent)

            else:
                user_prompt.select_option(pathlib.Path(os.getcwd()[option - 1]))

        else:
            print("Didn't select a folder.")
            choice = input("Do you want to exit? (y)")
            if choice.lower() == "y":
                break

    return None


if __name__ == '__main__':
    main()
