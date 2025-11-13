"""
Event handler module for arguments parsing and action execution.
"""

if __name__ == "__main__":
    raise RuntimeError("This module is not meant to be run directly. Please use the main script.")

import sys
from argparse import ArgumentError

from lib.args import ArgumentParser
from modules.kernels import KernelManager
from modules.packages import PackageManager
from modules.rootfs import RootFSManager
from modules.secure_boot import SecureBootManager
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
        print("[VERBOSE] Action set to:", args.action)
        print("[VERBOSE] Your platform is:", __get_current_platform())
        input("Press any key to continue.\n")


    match args.action:
        case "setup-secure-boot":
            SECURE_BOOT_MANAGER = SecureBootManager()
            PACKAGE_MANAGER = PackageManager()
            desktop_environment: str = PACKAGE_MANAGER.get_desktop_environment()

            SECURE_BOOT_MANAGER.install_dependencies(desktop_environment, args.verbose)
            SECURE_BOOT_MANAGER.backup_boot_files(args.verbose)
            SECURE_BOOT_MANAGER.install_shim(args.verbose)

        case "install-tkg-kernel":
            km = KernelManager(kernel_url="https://github.com/frogging-family/linux-tkg.git",
                               kernel_dir="linux-tkg")

            km.install_kernel(args.verbose)

        case "install-packages":
            pm = PackageManager()

            package_manager: str = pm.get_package_manager(args.verbose)
            desktop_environment: str = pm.get_desktop_environment()

            if args.verbose:
                print("[VERBOSE] Package manager to be used:", {package_manager})

            pm.install_packages(package_manager, desktop_environment, custom_pkglist=None)

        case "setup-rootfs":
            rfms = RootFSManager()

            rfms.install_files(args.verbose)

        case "setup-services":
            pm = PackageManager()
            sm = ServicesManager()
            desktop_environment = pm.get_desktop_environment()

            sm.enable_services(desktop_environment, args.verbose)
        case _:
            if not args.action:
                ARGUMENTS_PARSER.parser.print_help()
            else:
                raise ArgumentError(args.action, "Invalid action specified.")
