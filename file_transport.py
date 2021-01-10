# file_transport.py
"""Transport operations such as moving, copying and deleting."""

import os
import shutil
import send2trash


def main_copy():
    pass

def main_move():
    pass


class Delete:
    """Delete class for files and folders for my file explorer. Can be forgotten after process"""

    def __init__(self, items: list[str]):

        self.permission_direct_delete, self.ask_for_each_file = self.set_user_preference()
        self.deleted_files = []
        self.not_deleted_files = []

        for item in items:
            success = self.move2bin()
            self.item = item

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

    def set_user_preference(self) -> tuple[bool, bool]:
        """General user decision to give permission to delete files directly. Option to ask for every file."""
        print("Moving items to paper bin is on some systems not possible (Linux, BSD, etc.).",
              "Choose yes to decide for all files or each individually.", sep='\n')
        permission = input("\nCan I directly delete files in case they can't be moved to bin? (y or yes)")

        if permission.replace(' ', '').lower() in ('y', 'yes'):
            permission = True

            ask_again = input('\nAsk again for every file? (y or yes)')

            if ask_again.replace(' ', '').lower() in ('y', 'yes'):
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
        if shutil.rmtree.avoids_symlink_attacks():
            try:
                shutil.rmtree(self.item)

            except shutil.Error:
                return False
        else:
            print("Not safe to delete files.")
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
