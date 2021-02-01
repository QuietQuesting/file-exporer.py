"""My own commandline file explorer module in python
    Planning to be used for:
        - bulk renaming of files
        - automatic file sorting routines
        
"""

import os
import pathlib
import configparser

import output
import user_prompt


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
    In case you want to prompt the user to choose a folder/file use. """
    config = init_config()
    set_starting_dir(config)
    output.print_intro()

    option_inst = user_prompt.Options()

    while True:
        user_input = user_prompt.input_folder_num()

        if user_input[0] != -1:

            directory = pathlib.Path(os.getcwd())

            # open parent and continue next loop
            if len(user_input) == 1 and user_input[0] == 0:
                option_inst.select(directory.parent)

            else:
                # turns selected indexes to Path objects
                paths = [pathlib.Path(directory / os.listdir(directory)[item-1]) for item in user_input]
                option_inst.select(paths)

        else:
            print("You didn't select a folder.", end=' ')
            choice = input("Exit file explorer (y): ")
            if choice.lower() == "y":
                break

    return None


if __name__ == '__main__':
    main()
