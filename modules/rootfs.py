#!/usr/bin/env python3

"""
Module containing the RootFSManager class.
"""

import os
import getpass
import shutil

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
        self.current_user: str = getpass.getuser()

        if not override_permissions:
            if not self._is_admin():
                raise PermissionError(f"{self.current_user} doesn't have privileges to use" + \
                                      " {self.__class__.__name__} ")

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
                try:
                    file_path = os.path.join(path, file)
                    if verbose:
                        print(f"[VERBOSE] Added {file_path} to the list")
                    file_list.append(file_path)
                except Exception as e:
                    raise e
        return file_list

    def _copy_files(self, source: str, destination: str,
                    verbose: bool = False) -> None:
        """
        Copies the files to the respective directories.
        """
        if not source:
            raise ValueError("No source was provided.")

        if not self._is_directory(destination):
            raise FileNotFoundError(f"{destination} does not exist.")

        for root, _, files in os.walk(source):
            for file in files:
                file_path: str = os.path.relpath(os.path.join(root, file))
                file_relative_path: str = os.path.relpath(file_path, source)
                destination_path: str = os.path.join(destination, file_relative_path)
                is_dir: bool = os.path.isdir(os.path.dirname(destination_path))

                try:
                    if is_dir:
                        if verbose:
                            print(f"[VERBOSE] Copying '{file_path}' to '{destination_path}'...")

                        shutil.copyfile(file_path, destination_path)
                    else:
                        print(f"[ERROR] {os.path.dirname(destination_path)} does not exist")
                except Exception as e:
                    raise e

    def install_files(self, verbose: bool = False) -> None:
        """
        Installs the files to the respective directories.
        """
        paths: dict[str, str] = {
            "boot": "/boot",
            "etc": "/etc",
            "home": os.path.join("/home/", self.current_user),
            "usr": "/usr"
        }

        try:
            self._copy_files(self.local_dirs["boot_dir"], paths["boot"], verbose)
            self._copy_files(self.local_dirs["etc_dir"], paths["etc"], verbose)
            self._copy_files(self.local_dirs["home_dir"], paths["home"], verbose)
            self._copy_files(self.local_dirs["usr_dir"], paths["usr"], verbose)
        except Exception as e:
            raise e
