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

        if not getpass.getuser() == "root":
            raise PermissionError("current user does not have enough privileges.")

    def _is_directory(self, directory: str) -> bool:
        """
        Checks if a directory exists.
        """
        try:
            if os.path.isdir(directory):
                return True
            return False
        except Exception as e:
            raise e

    def _is_file(self, file: str) -> bool:
        """
        Checks if a file exists.
        """
        try:
            if os.path.isfile(file):
                return True
            return False
        except Exception as e:
            raise e

    def _create_list(self, from_directory: str,
                     to_list: list[str], verbose: bool = False) -> list[str]:
        """
        Creates a list from the specified directory.
        """

        for path, subdirs, files in os.walk(from_directory):
            subdirs: list[str] = [os.path.join(path, subdir) for subdir in subdirs]

            for file in files:
                file: str = os.path.join(path, file)
                match from_directory:
                    case self.boot_dir:
                        if verbose:
                            print(f"[VERBOSE] Added {file} to the list")
                        to_list.append(file)
                    case self.etc_dir:
                        if verbose:
                            print(f"[VERBOSE] Added {file} to the list {to_list}")
                        to_list.append(file)
                    case self.home_dir:
                        if verbose:
                            print(f"[VERBOSE] Added {file} to the list {to_list}")
                        to_list.append(file)
                    case self.usr_dir:
                        if verbose:
                            print(f"[VERBOSE] Added {file} to the list {to_list}")
                        to_list.append(file)
                    case _:
                        raise IOError(from_directory, "invalid directory")
        return to_list

    def _copy_files(self, from_list: list[str], verbose: bool = False) -> None:
        """
        Copies the files to the respective directories.
        """
        if not from_list:
            raise ValueError("No list was provided.")

        for file in from_list:
            match file:
                case self.boot_dir:
                    if verbose:
                        os.system(f"cp --backup -v {file} /boot")
                    else:
                        os.system(f"cp --backup {file} /boot")
                case self.etc_dir:
                    if verbose:
                        os.system(f"cp --backup -v {file} /etc")
                    else:
                        os.system(f"cp --backup {file} /etc")
                case self.home_dir:
                    if verbose:
                        os.system(f"cp --backup -v {file} /home")
                    else:
                        os.system(f"cp --backup {file} /home")
                case self.usr_dir:
                    if verbose:
                        os.system(f"cp --backup -v {file} /usr")
                    else:
                        os.system(f"cp --backup {file} /usr")
                case _:
                    raise IOError(file, "invalid file")

    def install_files(self, verbose: bool = False) -> None:
        """
        Installs the files to the respective directories.
        """
        boot_files: list[str] = []
        etc_files: list[str] = []
        home_files: list[str] = []
        usr_files: list[str] = []

        if verbose:
            boot_files = self._create_list(self.boot_dir, boot_files, True)
            etc_files = self._create_list(self.etc_dir, etc_files, True)
            home_files = self._create_list(self.home_dir, home_files, True)
            usr_files = self._create_list(self.usr_dir, usr_files, True)

        else:
            boot_files = self._create_list(self.boot_dir, boot_files)
            etc_files = self._create_list(self.etc_dir, etc_files)
            home_files = self._create_list(self.home_dir, home_files)
            usr_files = self._create_list(self.usr_dir, usr_files)
