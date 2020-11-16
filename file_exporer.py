"""My own commandline file explorer module in python
    Planning to be used for:
        - bulk renaming of files
        - automatic file sorting routines
        
        Arguments:
1st: Optional path of config.ini"""


import sys
import os
from typing import Union
import configparser
import output
import user_prompt
import file_transport
import delete


def get_argv1() -> Union[str, None]:
    """ Reads sys.argv[1] and returns it """
    try:
        argv = sys.argv[1]
        
    except IndexError:
        argv = None

    return argv


def init_config(name='config.ini') -> str:
    """initializes configparser object with consideration of sys.argv"""
    config = configparser.ConfigParser()
    config_file = get_argv1()
    
    if config_file and os.path.isfile(config_file):
        config.read(config_file)
        
    else:
        config.read(name)
        
    return config


def set_starting_dir(config) -> bool:
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
    return True


def run_file(file: str):
    """Executes runs file"""
    pass


def open_folder(folder: str) -> None:
    """Changes cwd to folder. Prints content of new folder."""
    os.chdir(folder)  # change to parent dir
    output.print_dir(folder)
    return None


def main() -> None:
    """ Main script flow of the file explorer.
    In case you want to prompt the user to choose a folder/file use fselect. """
    config = init_config()
    set_starting_dir(config)
    output.print_intro()

    running = True
    while running:
        option = input('\nEnter option: ')
        option = option.replace(' ', '').lower()

        if option.isdecimal():
            option = int(option)
            dir_list = os.listdir(os.getcwd())
            name = dir_list[option - 1]

            if os.path.isdir(dir_list[option-1]):

                print('Opening folder: {}'.format(name))
                open_folder(name)

            else:
                print('Opening file: \n')
                run_file(name)

        elif option in ('.', '..'):
            print('Opening parent folder.')
            open_folder('../')

        elif option in ('copy', 'c'):
            print('Option: copy file or folder:\n')

            selected = user_prompt.select()
            if not selected:  # User aborted process
                continue

            print('selected: {}'.format(selected))

        elif option in ('move', 'm'):
            print('Option: move file or folder:\n')
            selected = user_prompt.select()
            if not selected:  # User aborted process
                continue

            print('selected: {}'.format(selected))

        elif option in ('del', 'd'):
            print('Option: delete file or folder:\n')
            selected = user_prompt.select()
            if not selected:  # User aborted process
                continue

            print('selected: {}'.format(selected))

            delete.main(selected)

        elif option == 'help':
            output.print_options()

        elif option == 'exit':
            break
        else:
            print('Nothing.')

    return None


if __name__ == '__main__':
    main()
