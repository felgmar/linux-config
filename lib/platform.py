#!/usr/bin/env python3

"""
Module containing the Platform class.
"""

if __name__ == "__main__":
    print("This module is not meant to be run directly.")
    sys.exit(1)

import sys
import distro
import getpass
import platform

class Platform():
    """
    Class for detecting the current platform and distribution.
    """
    def __init__(self) -> None:
        self.CURRENT_DISTRO: str = distro.lsb_release_info().get("distributor_id", "unknown").lower()
        self.CURRENT_PLATFORM: str = platform.system().lower()
        self.CURRENT_USER = getpass.getuser()

    def __get_current_distro(self) -> str:
        return self.CURRENT_DISTRO

    def __get_current_platform(self) -> str:
        return self.CURRENT_PLATFORM

    def __get_current_user(self) -> str:
        return self.CURRENT_USER

    def get_platform(self) -> str:
        """
        Returns the current platform.
        """
        return self.__get_current_platform()

    def get_distro(self) -> str:
        """
        Returns the current distribution.
        """
        return self.__get_current_distro()

    def get_user(self) -> str:
        """
        Returns the current user.
        """
        return self.__get_current_user()
