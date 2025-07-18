#!/usr/bin/env python3

"""
Module containing the Platform class.
"""

if __name__ == "__main__":
    import sys
    print("This module is not meant to be run directly.")
    sys.exit(1)

class Platform:
    """
    Class for detecting the current platform and distribution.
    """
    def __get_current_distro(self) -> str:
        """
        Returns the current distribution.
        """
        try:
            import distro
            DISTRO_NOT_FOUND: str = "Failed to get the current distribution."
            CURRENT_DISTRIBUTION: str = distro.lsb_release_info().get("distributofr_id", DISTRO_NOT_FOUND).lower()

            if CURRENT_DISTRIBUTION == DISTRO_NOT_FOUND:
                raise RuntimeError(DISTRO_NOT_FOUND)
        except Exception as e:
            raise e

        return CURRENT_DISTRIBUTION
    def __get_current_platform(self) -> str:
        """
        Returns the current platform.
        """
        try:
            import platform
            CURRENT_PLATFORM: str = platform.system().lower()
        except Exception as e:
            raise e

        return CURRENT_PLATFORM

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
