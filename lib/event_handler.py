"""
Event handler module for arguments parsing and action execution.
"""

if __name__ == "__main__":
    raise RuntimeError("This module is not meant to be run directly. Please use the main script.")

import logging
import sys

from lib.args import ArgumentParser
from modules.packages import PackageManager
from modules.rootfs import RootFSManager
from modules.services import ServicesManager

ARGUMENTS_PARSER = ArgumentParser()
ARGUMENTS_PARSER.populate_args()
args = ARGUMENTS_PARSER.parse_args()

def __get_current_platform() -> str:
    """
    Get the current platform of the system.
    """
    return sys.platform.lower()

def __validate_platform() -> None:
    """
    Validate the current platform and raise an error if it is not supported.
    """
    ERROR_MESSAGE: str = __get_current_platform() + " is not a supported platform."
    assert __get_current_platform() == "linux", ERROR_MESSAGE

def __install_packages(verbose: bool = False) -> None:
    pm = PackageManager()

    package_manager: str = pm.get_package_manager(verbose)

    if verbose:
        print("[VERBOSE] Package manager was set to:", package_manager)

    pm.install_packages(package_manager)

def __enable_services(verbose: bool = False) -> None:
    SERVICE_MANAGER = ServicesManager()

    SERVICE_MANAGER.enable_services(verbose)

def __setup_rootfs(verbose: bool = False) -> None:
    rfms = RootFSManager()

    rfms.install_files(args.verbose)

def parse_actions() -> None:
    """
    Parse the action specified in the command line
    arguments and execute the corresponding function.
    """
    try:
        __validate_platform()
    except Exception as e:
        raise e

    if args.verbose:
        print("[VERBOSE] Your platform is:", __get_current_platform())
        input("Press any key to continue.\n")

    try:
        should_install_packages: bool = input("Do you want to install packages? (y/n): ").lower() == "y"
        if should_install_packages:
            __install_packages(args.verbose)
    except Exception as e:
        logging.error("An error has occurred while installing packages: %s", e)

    try:
        should_enable_services: bool = input("Do you want to enable services? (y/n): ").lower() == "y"
        if should_enable_services:
            __enable_services(args.verbose)
    except Exception as e:
        logging.error("An error has occurred while enabling services: %s", e)

    try:
        should_setup_rootfs: bool = input("Do you want to set up the root filesystem? (y/n): ").lower() == "y"
        if should_setup_rootfs:
            __setup_rootfs(args.verbose)
    except Exception as e:
        logging.error("An error has occurred while setting up the root filesystem: %s", e)
