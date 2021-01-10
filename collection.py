# collection.py
"""
Collection of different function which don't find under other names
"""

import os
import pathlib

def open_file(file: str):
    """Executes file"""
    print(f"simulating {file} opening.")


def open_folder(folder: str) -> None:
    """Changes cwd to folder. Prints content of new folder."""
    os.chdir(folder)  # change to parent dir
    output.print_dir(folder)
    return None


def open_parent() -> None:
    """Changes cwd to parent folder. Prints content of new folder."""
    current = pathlib.Path(os.getcwd())
    return current.parent