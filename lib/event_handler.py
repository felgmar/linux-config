"""
Event handler module for arguments parsing and action execution.
"""

import sys

from modules.kernels import KernelManager
from modules.packages import PackageManager
from modules.rootfs import RootFSManager
from modules.secure_boot import SecureBootManager
from modules.services import ServicesManager
from modules.args import ArgumentParser

ARGUMENTS_PARSER = ArgumentParser()
ARGUMENTS_PARSER.populate_args()
args = ARGUMENTS_PARSER.parse_args()

def _get_current_platform() -> str:
    """
    Get the current platform of the system.
    """
    return sys.platform.lower()

def _validate_platform() -> None:
    """
    Validate the current platform and raise an error if it is not supported.
    """
    assert _get_current_platform() == "linux", f"{_get_current_platform()} is not a supported platform."

def parse_actions() -> None:
    """
    Parse the action specified in the command line arguments and execute the corresponding function.
    """
    _validate_platform()

    if args.verbose:
        print("[VERBOSE] ⚠️ Action set to:", args.action)
        print("[VERBOSE] 💻 Your platform is:", _get_current_platform())
        input("Press any key to continue.\n")

    match args.action:
        case "setup-secure-boot":
            sbm = SecureBootManager()
            pm = PackageManager()

            if args.verbose:
                sbm.install_dependencies(pm.get_desktop_environment(), verbose=True)
                sbm.backup_boot_files(verbose=True)
                sbm.install_shim(verbose=True)
            else:
                sbm.install_dependencies(pm.get_desktop_environment())
                sbm.backup_boot_files()
                sbm.install_shim()

        case "install-tkg-kernel":
            pm = PackageManager()
            km = KernelManager(kernel_url="https://github.com/frogging-family/linux-tkg.git",
                                kernel_dir="linux-tkg")

            if args.verbose:
                km.install_kernel(verbose=True)
            else:
                km.install_kernel()

        case "install-packages":
            pm = PackageManager()

            PACKAGE_MANAGER = pm.get_package_manager(get_aur_helper=True)
            DESKTOP_ENVIRONMENT = pm.get_desktop_environment()

            if args.verbose:
                print("[VERBOSE] Package manager to be used:", {PACKAGE_MANAGER})

            pm.install_packages(PACKAGE_MANAGER, DESKTOP_ENVIRONMENT, custom_pkglist=None)

        case "setup-rootfs":
            rfms = RootFSManager()
            
            if args.verbose:
                rfms.install_files(verbose=True)
            else:
                rfms.install_files()

        case "setup-services":
            pm = PackageManager()
            sm = ServicesManager()
            services = sm.get_services_list(desktop_environment=None)

            sm.enable_services(services)

        case _:
            if not args.action:
                raise ValueError("No action was specified.")
            raise ValueError(args.action, "invalid action")
