#!/usr/bin/env python3

"""
Module containing the RootFSManager class.
"""

import os
import getpass
import shutil
import sys

from lib.platform import Platform

class RootFSManager():
    """
    Handles files customized by the user.
    """
    def __init__(self):
        self.local_dirs: dict[str, str] = {
            "boot_dir": os.path.join(os.getcwd() + '/modules/rootfs/boot'),
            "etc_dir": os.path.join(os.getcwd() + '/modules/rootfs/etc'),
            "home_dir": os.path.join(os.getcwd() + '/modules/rootfs/home'),
            "usr_dir": os.path.join(os.getcwd() + '/modules/rootfs/usr'),
        }
        self.CURRENT_USER: str = getpass.getuser()
        self.CURRENT_DISTRO = Platform().get_distro()
        self.CURRENT_PLATFORM = Platform().get_platform()

        if not self.CURRENT_PLATFORM == "linux":
            print(f"[!] This script is only meant to run on Linux, not {self.CURRENT_PLATFORM}.")
            sys.exit(1)

        if not self.__is_admin():
            raise PermissionError("You must run this module as root to modify system files.")

    def __is_admin(self) -> bool:
        """
        Checks if the current user is an administrator.
        """
        if getpass.getuser() == "root":
            return True
        return False

    def __is_directory(self, directory: str) -> bool:
        """
        Checks if a directory exists.
        """
        try:
            if os.path.isdir(directory):
                return True
            return False
        except Exception as e:
            raise e

    def __is_file(self, file: str) -> bool:
        """
        Checks if a file exists.
        """
        try:
            return os.access(file, os.R_OK)
        except Exception as e:
            raise e

    def __is_writable(self, file: str) -> bool:
        """
        Checks if a file is writable.
        """
        try:
            return os.access(file, os.W_OK)
        except Exception as e:
            raise e

    def __create_list(self, from_directory: str, verbose: bool = False) -> list[str]:
        """
        Creates a list from their specified directory type.
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

    def __copy_files(self, source: str, destination: str,
                    verbose: bool = False) -> None:
        """
        Copies the files to their respective directories.
        """
        if not source:
            raise ValueError("No source was provided.")
        
        if not destination:
            raise ValueError("No destination was provided.")

        if not self.__is_directory(destination):
            raise FileNotFoundError(destination, "does not exist.")
        
        if source == destination:
            raise ValueError("Source and destination cannot be the same.")
        
        if self.CURRENT_DISTRO == "fedora" and destination == "/boot":
            print(f"[!] {self.CURRENT_DISTRO} does not use systemd-boot, skipping boot files.")

        file_list: list[str] = self.__create_list(source, verbose)

        for file in file_list:
            source_path: str = os.path.relpath(file)
            file_relative_path: str = os.path.relpath(source_path, source)
            destination_path: str = os.path.join(destination, file_relative_path)
            is_dir: bool = os.path.isdir(os.path.dirname(destination_path))

            try:
                assert self.__is_file(source_path), f"{source_path} is not a file."

                if not self.__is_writable(destination_path):
                    return

                if is_dir:
                    if verbose:
                        print(f"[VERBOSE] Backup up '{destination_path}' to '{destination_path}.backup'...")
                    shutil.copyfile(destination_path, f"{destination_path}.backup")
                    
                    if verbose:
                        print(f"[VERBOSE] Copying '{source_path}' to '{destination_path}'...")
                    shutil.copyfile(source_path, destination_path)
                else:
                    print(f"[!] Skipped directory {os.path.dirname(destination_path)}, since it does not exist.")
            except Exception as e:
                raise e

    def install_files(self, verbose: bool = False) -> None:
        """
        Installs the files to the respective directories.
        """
        paths: dict[str, str] = {
            "boot": "/boot",
            "etc": "/etc",
            "home": os.path.join("/home/", self.CURRENT_USER),
            "usr": "/usr"
        }

        try:
            self.__copy_files(self.local_dirs["boot_dir"], paths["boot"], verbose)
            self.__copy_files(self.local_dirs["etc_dir"], paths["etc"], verbose)

            if not self.CURRENT_USER == "root":
                self.__copy_files(self.local_dirs["home_dir"], paths["home"], verbose)
            else:
                print("[!] Running as root, not copying home files.")

            self.__copy_files(self.local_dirs["usr_dir"], paths["usr"], verbose)
        except Exception as e:
            raise e
