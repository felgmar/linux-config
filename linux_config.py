#!/usr/bin/env python3

"""
Main file for the Linux configuration script.
"""

import sys
import argparse

from modules.kernels import KernelManager
from modules.packages import PackageManager
from modules.rootfs import RootFSManager
from modules.secure_boot import SecureBootManager
from modules.services import ServicesManager

CURRENT_PLATFORM = sys.platform.lower()

actions: list[str] = [
    "setup-secure-boot", "install-tkg-kernel",
    "install-packages", "setup-rootfs", "setup-services"
]

parser = argparse.ArgumentParser(prog="linux-config")
group = parser.add_mutually_exclusive_group()

parser.add_argument("-a", "--action", choices=actions, type=str,
                    help="Runs the specified script. Available options are " +
                    ", ".join(actions), metavar="")

group.add_argument("-d", "--distro", type=str,
                   help="Specifies which distro is going to be modified." +
                   " (e.g. arch, fedora, debian)", metavar="")

parser.add_argument("-v", "--verbose", action="store_true", help="Print more messages")

group.add_argument("--version", action="version", version="%(prog)s 1.0")

args = parser.parse_args()

if __name__ == "__main__":
    if CURRENT_PLATFORM != "linux":
        raise RuntimeError(CURRENT_PLATFORM, "platform not supported")

    if args.verbose:
        print(f"[i] Action set to: {args.action}\n[i] Distribution set to: {args.distro}\n")
        print("Press any key to continue.")
        input()

    try:
        match args.action:
            case "setup-secure-boot":
                sbm = SecureBootManager()
                pm = PackageManager()

                if args.verbose:
                    sbm.install_dependencies(verbose=True)
                    sbm.backup_boot_files(verbose=True)
                    sbm.install_shim(verbose=True)
                else:
                    sbm.install_dependencies()
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
                PACKAGE_MANAGER = pm.get_package_manager(override_package_manager=True)

                if args.verbose:
                    print("[i] Package manager to be used:", {PACKAGE_MANAGER})

                pm.install_packages(PACKAGE_MANAGER)

            case "setup-rootfs":
                rfsm = RootFSManager()

                if args.verbose:
                    rfsm.copy_files(verbose=True)
                else:
                    rfsm.copy_files()

            case "setup-services":
                pm = PackageManager()
                sm = ServicesManager()
                DESKTOP_ENVIRONMENT = pm.desktop_environment

                services = sm.get_services_list(DESKTOP_ENVIRONMENT)

                sm.enable_services(services)

            case _:
                if not args.action:
                    raise ValueError("No action was specified.")
                raise ValueError(f"{args.action}: invalid action")
    except Exception as e:
        raise e
