# item_operations.py
"""Transport operations such as moving, copying and deleting."""

import os
import pathlib
import shutil
import mimetypes
import subprocess
from typing import Union

import LnkParse3
import send2trash

import output


class Copy:
    """Copy items to the destinations given. items must be """

    def __init__(self, items: list[Union[os.PathLike, pathlib.Path]], dest: str):
        if isinstance(items, str):
            self.items = [items]
        self.items = items
        self.follow_sym = True
        self.paste(dest)

    def paste(self, dest):
        """Not used rn."""
        for item in self.items:
            if os.path.isfile(item):
                shutil.copy2(item, dest, follow_symlinks=self.follow_sym)
            else:
                shutil.copytree(item, dest, self.follow_sym)


class Move(Copy):
    def __init__(self, items, dest):
        super(Copy, self).__init__(items, dest)

    def paste(self, destination):
        for item in self.items:
            if os.path.isfile(item):
                shutil.copy2(item, destination, follow_symlinks=self.follow_sym)
            else:
                shutil.copytree(item, destination, ignore_dangling_symlinks=True, dirs_exist_ok=True)

        Delete(self.items)


class Delete:
    """Delete class for files and folders for my file explorer. Can be forgotten after process"""

    def __init__(self, items: list[str]):

        self.permission_direct_delete, self.ask_for_each_file = self.set_user_preference()
        self.deleted_files = []
        self.not_deleted_files = []

        if isinstance(items, str):
            items = [items]

        for item in items:

            self.item = str(item)
            success = self.move2bin()

            if not success:

                if self.permission_direct_delete:

                    if self.ask_for_each_file:

                        if self.get_delete_permission():
                            success = self.delete()

                    else:  # permission to delete without asking
                        success = self.delete()

            if success:
                self.deleted_files.append(self.item)

            else:
                self.not_deleted_files.append(item)

        print("Finished! Successfully deleted:", *self.deleted_files, sep='\n')
        print("\nFailed to delete:", *self.not_deleted_files, sep='\n')

    @staticmethod
    def set_user_preference() -> tuple[bool, bool]:
        """General user decision to give permission to delete files directly. Option to ask for every file."""
        print("Moving items to paper bin is on some systems not possible (Linux, BSD, etc.).",
              "Choose yes to decide for all files or each individually.", sep='\n')
        permission = input("\nDelete files directly in case they can't be moved to bin? (y)")

        if permission.replace(' ', '').lower() == 'y':
            permission = True

            ask_again = input('\nAsk again for every file? (y)')

            if ask_again.replace(' ', '').lower() == 'y':
                ask_again = True

            else:
                ask_again = False

        else:
            permission = ask_again = False

        return permission, ask_again

    def get_delete_permission(self) -> bool:
        """Asks for user choice to delete file"""
        choice = input("\nCouldn't move {} to paper bin, try to delete it directly (y, yes)?".format(self.item))

        if choice.replace(' ', '').lower() in ('y', 'yes'):
            print("Deleting file.")
            return True

        print("Not deleting file.")
        return False

    def move2bin(self):
        """Send item to bin with send to trash module.
        Exception:
            send2trash.TrashPermissionError:        Raised on freedesktop platforms when send2trash is not effective.
                                                    Deleting them directly if permission granted
            OSError:                                Access Error, File not found or something else."""
        try:
            send2trash.send2trash(self.item)

        except send2trash.TrashPermissionError:
            return False

        except OSError:
            return False
        return True

    def delete(self) -> bool:
        """Checks whether item is folder or file and calls the right function."""
        if os.path.isfile(self.item):
            return self.delete_file()

        else:
            return self.delete_folder()

    def delete_folder(self) -> bool:
        """Deletes file and handles every exception
        Exceptions:
            OSError:        rmdir() only seems to delete empty folders. In that case we try to delete tree with shutil
        """
        try:
            os.rmdir(self.item)
            return True

        except FileNotFoundError:
            return False

        except OSError:
            return self.delete_tree()

    def delete_tree(self) -> bool:
        """Deletes dir with rmtree. Handles shutil exceptions"""
        if shutil.rmtree.avoids_symlink_attacks:
            try:
                shutil.rmtree(self.item)

            except shutil.Error:
                return False
        else:
            print("Delete function is not symlink attack resistant on this system.")
            print(f"Not deleting {self.item}")
            return False

        return True

    def delete_file(self) -> bool:
        """Deletes file directly and handles every exception."""
        try:
            os.remove(self.item)

        except PermissionError:
            print("No permission to delete item.", "Skipping item: ", self.item, sep="\n")
            return False

        except IsADirectoryError:
            return self.delete_folder()

        except OSError:  # test if this gets called when path is wrong. If not use FileNotFoundError exception
            print("Something else went wrong when deleting.", "Skipping item: ", self.item, sep="\n")
            return False

        return True

    def get_status(self):
        """Returns the success rate as a num"""
        deleted = len(self.deleted_files)
        not_deleted = len(self.not_deleted_files)
        total = deleted + not_deleted
        return deleted / total


class Open:
    def __init__(self, paths):
        """Checks the type of the item and calls the associated function to open it."""
        self.open_item(paths)

    def open_item(self, paths):
        for path in paths:
            if path.is_dir():
                self.open_folder(path)

            elif path.name[:-4] == '.lnk':
                path = get_link_destination(path)
                self.open_item([path])

            elif path.name[:-4] == ".url":
                self.open_file(path)

            else:
                self.open_file(path)

    @staticmethod
    def open_file(file: Union[os.PathLike, str, pathlib.Path]) -> None:
        """Executes file"""
        file = f"'{str(file)}'"
        subprocess.run([file])

    @staticmethod
    def open_folder(folder: Union[os.PathLike, str, pathlib.Path]) -> None:
        """Changes cwd to folder. Prints content of new folder."""
        os.chdir(folder)  # change to parent dir
        output.print_dir(folder)

    @staticmethod
    def open_parent() -> None:
        """Changes cwd to parent folder. Prints content of new folder."""
        return os.chdir(pathlib.Path(os.getcwd()).parent)


def get_link_destination(file) -> str:
    """Changes cwd to destination of .lnk"""
    with open(file, "rb") as indata:
        parser_inst = LnkParse3.lnk_file(indata)

    file_info = parser_inst.get_json(False)

    return file_info["link_info"]["local_base_path"]


class Create:
    def __init__(self, items: list[pathlib.Path], item_type: str):
        """
        @param items: list of paths
        @param item_type: must bei either "folder" or "sub directory"
        """
        item_type = item_type.lower()
        if item_type not in ("file", "sub directory"):
            raise TypeError(f"Can't create {item_type}, only folder or sub directory.")

        if len(items) > 1:
            ask_again = self.get_ask_again_choice()
        else:
            ask_again = False

        self.item_type = item_type

        name = self.get_first_name(items[0])
        amount = 0

        for item in items:
            # Can't make a folder within a file. Skip to next one
            self.item = item
            if not os.path.isdir(self.item):
                continue

            if ask_again:
                name = self.get_next_name()

            success = self.create_item(name)

            if success:
                amount += 1

        self.success_rate = amount / len(items)
        print("Done.\n")

    def get_ask_again_choice(self) -> bool:
        """General user decision ask for a name for every item."""
        print("")
        choice = input(f"Choose a name for every new {self.item_type}? (y, yes)")

        if choice.lower() in ("y", "yes"):
            return True

        return False

    def create_item(self, name) -> bool:
        """Calls the create function for the associated type"""

        if self.item_type == "file":
            return self.create_file(name)

        else:
            return self.create_folder(name)

    def create_file(self, name) -> bool:
        try:
            with open(self.item / name, "w"):
                pass

        except Exception:
            return False
        return True

    def create_folder(self, name):
        """ Create a folder in current path"""
        try:
            os.mkdir(self.item / name)
        except FileExistsError:
            print("Dir already exists.")
            return False
        return True

    def get_first_name(self, parent):
        """Ask for the first name and returns it"""
        name = input(f"Enter the first name for {self.item_type} with in {parent}:")

        while not self.name_ok(name):
            print('Following characters are not allowed \\ / : * " ? < > |')
            name = input(f"Enter a valid name for {self.item_type} with in {parent}: ")

        return name

    def get_next_name(self):
        """Asks for the next name and returns it"""
        name = input(f"Enter the next name for {self.item_type} with in {self.item.parent}:")

        while not self.name_ok(name):
            print('Following characters are not allowed \\ / : * " ? < > |')
            name = input(f"Enter a valid name for {self.item_type} with in {self.item.parent}: ")

        return name

    @staticmethod
    def name_ok(string: str) -> bool:
        """checks if string is okay as a folder name"""
        if string != "":
            for letter in string:
                if letter in ("\\", "/", ":", "*", '"', "?", "<", ">", "|"):
                    return False
            return True
        return False


def get_mimetype(file):
    """Gets the mimetype, with mimetypes.guess_type and my own special cases"""
    if os.path.isdir(file):
        _type = 'directory/folder'

    elif file[-4:] == '.lnk':
        _type = 'shortcut/local'

    elif file[-4:] == '.url':
        _type = 'shortcut/url'

    elif os.path.isfile(file):
        # Get Mimetype as tuple, want only first tuple item. Is None if no matches
        _type = mimetypes.guess_type(file, strict=False)[0]

    else:
        _type = None

    if _type is None:
        _type = 'unknown/uncommon'

    return _type
