#!/usr/bin/env python3

"""
Module containing the RootFSManager class.
"""

import os
import getpass

class RootFSManager():
    """
    Handles files customized by the user.
    """
    def __init__(self):
        self.rootfs_dir: str = os.path.join(os.getcwd() + '/modules/rootfs')
        self.boot_dir: str = os.path.join(self.rootfs_dir, "boot")
        self.etc_dir: str = os.path.join(self.rootfs_dir, 'etc')
        self.home_dir: str = os.path.join(self.rootfs_dir, 'home')
        self.usr_dir: str = os.path.join(self.rootfs_dir, 'usr')
        self.boot_files: list[str] = []
        self.etc_files: list[str] = []
        self.home_files: list[str] = []
        self.usr_files: list[str] = []

        assert getpass.getuser() == "root", \
            f"{self.__class__.__name__}: current user does not have enough privileges."

    def _check_directory_exists(self, directory: str) -> bool:
        """
        Checks if a directory exists.
        """
        try:
            if os.path.isdir(directory):
                return True
            return False
        except Exception as e:
            raise e
    def _check_file_exists(self, file: str) -> bool:
        """
        Checks if a file exists.
        """
        try:
            if os.path.isfile(file):
                return True
            return False
        except Exception as e:
            raise e

    def _fill_lists(self, directory: str, verbose: bool = False) -> None:
        """
        Fills the lists with the files to be copied.
        """
        try:
            for path, subdirs, files in os.walk(directory):
                subdirs: list[str] = [os.path.join(path, subdir) for subdir in subdirs]

                if verbose:
                    print(f"[VERBOSE] Subdirectories: {subdirs}")
                    print(f"[VERBOSE] Files: {files}")

                for file in files:
                    file = os.path.join(file, path)
                    match directory:
                        case self.boot_dir:
                            if verbose:
                                print(f"[VERBOSE] Added {file} to the list boot_files")
                            self.boot_files.append(file)
                        case self.etc_dir:
                            if verbose:
                                print(f"[VERBOSE] ({list}) Added {file} to the list etc_files")
                            self.etc_files.append(file)
                        case self.home_dir:
                            if verbose:
                                print(f"[VERBOSE] ({list}) Added {file} to the list home_files")
                            self.home_files.append(file)
                        case self.usr_dir:
                            if verbose:
                                print(f"[VERBOSE] ({list}) Added {file} to the list usr_files")
                            self.usr_files.append(file)
                        case _:
                            raise IOError(directory, "invalid directory")
        except Exception as e:
            raise e

    def copy_files(self, verbose: bool = False) -> None:
        """
        Copies the files to the respective directories.
        """
        try:
            for directory in self.boot_dir, self.etc_dir, self.home_dir, self.usr_dir:
                if verbose:
                    self._fill_lists(directory, verbose)
                else:
                    self._fill_lists(directory)
        except Exception as e:
            raise e

        try:
            for directory in self.boot_dir, self.etc_dir, self.home_dir, self.usr_dir:
                match directory:
                    case self.boot_dir:
                        for file in self.boot_files:
                            if verbose:
                                os.system(f"cp --backup -v {file} /boot")
                            else:
                                os.system(f"cp --backup {file} /boot")
                    case self.etc_dir:
                        for file in self.etc_files:
                            if verbose:
                                os.system(f"cp --backup -v {file} /etc")
                            else:
                                os.system(f"cp --backup {file} /etc")
                    case self.home_dir:
                        for file in self.home_files:
                            if verbose:
                                os.system(f"cp --backup -v {file} /home")
                            else:
                                os.system(f"cp --backup {file} /home")
                    case self.usr_dir:
                        for file in self.usr_files:
                            if verbose:
                                os.system(f"cp --backup -v {file} /usr")
                            else:
                                os.system(f"cp --backup {file} /usr")
                    case _:
                        raise Exception(directory, "invalid directory")
        except Exception as e:
            raise e
