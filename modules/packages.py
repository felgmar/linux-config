#!/usr/bin/env python3

"""
Module containing the PackageManager class.
"""

import subprocess
import shutil

from lib.platform import Platform

class PackageManager():
    """
    Manages the installation of packages.
    """
    def __init__(self):
        self.PLATFORM: Platform = Platform()
        self.CURRENT_DISTRO: str = self.PLATFORM.get_distro()
        self.CURRENT_USER: str = self.PLATFORM.get_user()

    def get_package_manager(self, verbose: bool = False) -> str:
        """
        Returns the package manager based on the current distribution.
        """
        PACKAGE_MANAGER: str | None = shutil.which("apt")

        if PACKAGE_MANAGER is None:
            raise ValueError("No package manager could be set.")

        return PACKAGE_MANAGER

    def convert_list_to_str(self, list: list[str]) -> str:
        """
        Converts a list to a string.
        """
        new_string: str = ' '.join(list)

        return new_string

    def get_package_list(self) -> list[str]:
        """
        Returns a list of packages based on the desktop environment.
        """
        match self.CURRENT_DISTRO:
            case "ubuntu":
                return [
                    "git",
                    "lutris",
                    "cifs-utils",
                    "remmina"
                ]
            case _:
                raise ValueError(self.CURRENT_DISTRO, "unsupported distro")

    def install_packages(self, package_manager: str) -> None:
        """
        Installs packages based on the current distribution.
        """
        packages: list[str] = self.get_package_list()
        command: list[str] = []

        command.append("sudo")
        command.append(package_manager)
        command.extend(["install", "-y"])
        command.extend(packages)

        try:
            subprocess.run(command)
        except Exception as e:
            raise e
