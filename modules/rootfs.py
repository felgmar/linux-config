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
    def __init__(self, override_permissions: bool = False):
        self.local_dirs: dict[str, str] = {
            "boot_dir": os.path.join(os.getcwd() + '/modules/rootfs/boot'),
            "etc_dir": os.path.join(os.getcwd() + '/modules/rootfs/etc'),
            "home_dir": os.path.join(os.getcwd() + '/modules/rootfs/home'),
            "usr_dir": os.path.join(os.getcwd() + '/modules/rootfs/usr'),
        }        
        self.CURRENT_USER: str = getpass.getuser()

        if not override_permissions:
            if not self._is_admin():
                raise PermissionError(f"{self.CURRENT_USER} doesn't have privileges to use {self.__class__.__name__} ")

    def _is_admin(self) -> bool:
        """
        Checks if the current user is an administrator.
        """

        if getpass.getuser() == "root":
            return True
        return False

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

    def _create_list(self, from_directory: str, verbose: bool = False) -> list[str]:
        """
        Creates a list from the specified directory type.
        """
        file_list: list[str] = []

        for path, _, files in os.walk(from_directory):
            for file in files:
                file_path = os.path.join(path, file)
                if verbose:
                    print(f"[VERBOSE] Added {file_path} to the list")
                file_list.append(file_path)
        return file_list

    def _copy_files(self, from_list: list[str], destination: str, verbose: bool = False) -> None:
        """
        Copies the files to the respective directories.
        """
        if not from_list:
            raise ValueError("No list was provided.")
        
        if not self._is_directory(destination):
            raise FileNotFoundError("Destination directory does not exist.")

        for file in from_list:
            if verbose:
                print(f"[VERBOSE] Copying {file} to {destination}")
                command: str = f"cp --backup -v {file} {destination}"
            else:
                command: str = f"cp --backup {file} {destination}"
            
            os.system(command)

    def install_files(self, verbose: bool = False) -> None:
        """
        Installs the files to the respective directories.
        """
        IS_VERBOSE: bool = True if verbose else False

        filesystem_paths = {
            "boot": "/boot",
            "etc": "/etc",
            "home": os.path.join("/home/", self.CURRENT_USER),
            "usr": "/usr"
        }

        boot_files: list[str] = []
        etc_files: list[str] = []
        home_files: list[str] = []
        usr_files: list[str] = []

        boot_files = self._create_list(self.local_dirs["boot_dir"], IS_VERBOSE)
        etc_files = self._create_list(self.local_dirs["etc_dir"], IS_VERBOSE)
        home_files = self._create_list(self.local_dirs["home_dir"], IS_VERBOSE)
        usr_files = self._create_list(self.local_dirs["usr_dir"], IS_VERBOSE)

        self._copy_files(boot_files, filesystem_paths["boot"], IS_VERBOSE)
        self._copy_files(etc_files, filesystem_paths["etc"], IS_VERBOSE)
        self._copy_files(home_files, filesystem_paths["home"], IS_VERBOSE)
        self._copy_files(usr_files, filesystem_paths["usr"], IS_VERBOSE)
