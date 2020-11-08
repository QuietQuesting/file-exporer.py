# delete.py
"""Delete functions for files and folders for my file explorer."""

import os
import shutil
import send2trash


def main(items: list[str]):
    """Main flow for deleting files and folders."""
    permission_direct_delete, ask_for_each_file = get_user_preference()
    deleted_files = not_deleted_files = []

    for item in items:
        success = move2bin(item)
        if not success:

            if permission_direct_delete:

                if ask_for_each_file:

                    if get_delete_permission(item):
                        success = delete(item)

                else:  # permission to delete without asking
                    success = delete(item)

        if success:
            deleted_files.append(item)
        else:
            not_deleted_files.append(item)


def get_user_preference() -> tuple[bool, bool]:
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


def get_delete_permission(file: str) -> bool:
    """Asks for user choice to delete file"""
    choice = input("\nCouldn't move {} to paper bin, try to delete it directly (y, yes)?".format(file))

    if choice.replace(' ', '').lower() in ('y', 'yes'):

        print("Deleting file.")
        return True

    print("Not deleting file.")
    return False


def move2bin(item: str):
    """Send item to bin with send to trash module.
    Exception:
        send2trash.TrashPermissionError:        Raised on freedesktop platforms when send2trash is not effective.
                                                Deleting them directly if permission granted
        OSError:                                Access Error, File not found or something else."""
    try:
        send2trash.send2trash(item)

    except send2trash.TrashPermissionError:
        return False

    except OSError:
        return False
    return True


def delete(item: str) -> bool:
    """Checks whether item is folder or file and calls the right function."""
    if os.path.isfile(item):
        return delete_file(item)

    else:
        return delete_folder(item)


def delete_folder(item: str) -> bool:
    """Deletes file and handles every exception
    Exceptions:
        OSError:        rmdir() only seems to delete empty folders. In that case we try to delete tree with shutil
    """
    try:
        os.rmdir(item)
        return True

    except FileNotFoundError:
        return False

    except OSError:
        return delete_tree(item)


def delete_tree(item) -> bool:
    """Deletes dir with rmtree. Handles exceptions"""
    if shutil.rmtree.avoids_symlink_attacks():
        try:
            shutil.rmtree(item)

        except shutil.Error:
            return False
    else:
        print("Not safe to delete files.")
        return False

    return True


def delete_file(item: str) -> bool:
    """Deletes file and handles every exception."""
    try:
        os.remove(item)

    except PermissionError:
        print("No permission to delete item.", "Skipping item: ", item, sep="\n")
        return False

    except IsADirectoryError:
        return delete_folder(item)

    except OSError:  # test if this gets called when path is wrong. If not use FileNotFoundError exception
        print("Something else went wrong when deleting.", "Skipping item: ", item, sep="\n")
        return False

    return True
