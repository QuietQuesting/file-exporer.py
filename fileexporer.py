"""My own commandline file explorer module in python
    Planning to be used for:
        - bulk renaming of files
        - automatic file sorting routines
        
        Arguments:
1st: Optional path of config.ini"""


import sys
import os
import mimetypes
import shutil
from platform import system
from hashlib import sha1
from send2trash import send2trash
import configparser
import pdb



def read_argv() -> str:
    """ Reads and returns sys.argv.
        In Linux sys.argv is given bitwise decoding it in utf-8
        Not sure how it works in MacOS, asuming same as Windows."""
    try:
        argv = sys.argv[1]
        
    except IndexError:
        argv = None

    if system() == 'Linux':
        decoder = sha1()
        decoder.update(bytes(argv, 'utf-8'))
        return decoder.hexdigest()
    
    else:
        return argv


def init_config(name='config.ini') ->str:
    """initializes configparser object with concideration of sys.argv""" 
    config = configparser.ConfigParser()
    config_file = read_argv()
    
    if config_file and os.path.isfile(config_file):
        config.read(config_file)
        
    else:
        config.read(name)
        
    return config


def get_starting_dir(config) ->bool:
    """ Looks for starting directory in config
    requires returned class from init_config
    Returns directory or else an empty string"""
    try:
        starting_dir = config['DEFAULT']['starting_dir']
        
    except:
        return False

    if not starting_dir or not os.path.isdir(starting_dir):
        return False
    
    else:
        os.chdir(starting_dir)
        return True

def print_dir(folder=os.getcwd()) ->None:
    """Fancy prints directory and it's content."""
    intro = '\nContent of folder: {}'.format(folder)
    
    print(intro)
    print('o', len(intro) * '-',sep='')

    print(f'| ...\tparent folder:\t{parent_dir(folder):20}')
    
    for index, item in enumerate(os.listdir(folder)):
        path = folder + '\\' + item
        
        if item[-4:] == '.lnk':
            _type = 'link/shortcut'
            
        elif os.path.isfile(path):
            # Get Mimetype as tuple, want only first tuple item
            _type = mimetypes.guess_type(path, strict=False)[0]

            if _type == None:
                _type = 'unknown/uncommon'

        else:
            _type = 'dir/folder'
            
        print(f'| {index+1:02}.\t{item:20}{_type}')
        
    return None

    
def input_num(number=-1)-> int:
    """ Accepts numbers within range of cwd.
    Special nums: 0 counts as abort. -1 as confirm."""
    dir_list = os.listdir(os.getcwd())
        
    while not (-1 < number <= len(dir_list)):

        number = input('Enter your number now: ')
        
        try:
            number = int(number)

        except ValueError:  
            print('That is not a number.')
            
        if number == '':
            return -1
            
        elif number in ('..', '.'):
            return -2
            
        print('Number out of range! Input number between 1 - {}.'.format(len(dir_list)))
        
    return number


def fselect(count=1) ->list[str]:
    """Prompt user to select file or folder."""
    print('Please input a number to open the associated folder or select the file.')
    print('Else input 0 to cancel and enter to choose the current folder.')
    print('Else enter ".." to go back up')

    selection = []
    
    print(f'Please select {count} folder or files, one after the other')
    for i in range(count):

        selected = False
        
        while not selected:
            num = input_num()

            if num == 0:
                print('Aborting process.')
                return 0
            
            elif num == -1:
                print('Current folder is selected!')
                selection.append(f)
                selected = True

            elif num == -2:
                os.chdir(parent_dir())
                print("Going to parent folder.")
                print_dir()

            else:   # open folder / ask if user wants to select this file
                dir_list = os.listdir(os.getcwd())
                file = dir_list[num-1] # file or folder
                
                if os.path.isfile(f):
                    choice = input(f'Do you want to select {f}? (y,n)')
                    
                    if choice.replace(' ', '').lower() in ('y', 'yes', 'yeah'):
                        print('File selected')
                        selection.append(f)
                        selected = True
                    
                    else:
                        print('File not selected.\n')
                else:
                    os.chdir(os.getcwd() + '\\' + file)
                    print('Going into selected folder:')
                    print(f)
                    print_dir()
    return selected
        
            

def fopen(number) -> bool:
    """Opens n-st file or folder in cwd.
        Todo: test if symlinks (.lnk) open"""
    direcory = os.getcwd()
    
    path = direcory + '\\' + dir_list[number-1]
    
    if os.path.isfile(path):
        
        return False
    
    else:
        list_dir()
        os.chdir(path)
        return True

            
def parent_dir(directory=os.getcwd) ->str:
    """Returns the parent-directory as a string."""
    last_slash = directory.rfind('\\')
    
    if last_slash != -1:
        return directory[:last_slash]
    
    raise OSError('Can\'t go back up!')


def print_intro() ->None:
    """ Simple introduction used at the start of main."""
    print('===========================')
    print('Welcome to my file exporer!')
    print('===========================')
    print('Please choose one of the following options:\n')
    
    print_options(intro=True)
    print_dir()
    return None


def print_options(intro=False) ->None:
    """ Prints all current options user can use."""
    if not intro:
        print('\nYou can choose following options:\n')
    print('Enter number to open associated folder or file.')
    print('Enter ".." to open parent folder.')
    print('co / copy to copy file/folder')
    print('m / move to crop file/folders')
    print('del to delete file/folders')
    
    return None

    
def main():
    """ Main script flow of the file explorer.
    In case you want to prompt the user to choose a folder/file use fselect. """
    config = init_config()
    get_starting_dir(config)
    print_intro()

    running = True
    while running:
        option = input('\nEnter option: ')
        option = option.replace(' ', '').lower()

        if option.isdecimal():
            option = int(option)
            
            file = input_num(option)
            dir_list = os.listdir(os.getcwd())
            
            if os.path.isdir(dir_list[option-1]):
                print('Opening folder: {}'.format(dir_list[option-1]))
                os.chdir(os.getcwd() + '\\' + dir_list[option-1])
                print_dir()
                
            else:
                print('Opening file: ')

        elif option in ('.', '..'):
            print('Opening parent folder.')
            print_dir()
            os.chdir(parent_dir())    
            
        elif option in ('copy', 'c'):
            print('Option: copy file or folder')
            print(f'selected: {fselect(2)}')
        
        elif option in ('move', 'm'):
            print('Option: move file or folder')
            print(f'selected: {fselect(2)}')
            pass
        
        elif option in ('del', 'd'): 
            print('Option: delete file or folder')
            print(f'selected: {fselect()}')

        elif option == 'help':
            print_options()
        else:
            print('Nothing.')
            
    return None


if __name__ == '__main__':
    main()
            
        
