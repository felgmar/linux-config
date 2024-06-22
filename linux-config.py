#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getuser
from sys import platform

from modules.kernels.setup import KernelInstaller
from modules.packages.setup import PackageManager
from modules.tools.secure_boot.setup import SecureBootManager
from modules.tools.services_manager.setup import ServicesManager

current_platform = platform.lower()

actions = [
    "setup-secure-boot", "install-tkg-kernel",
    "install-packages", "install-packages",
    "setup-rootfs", "setup-services"
]

parser = ArgumentParser(prog="linux-config")
group = parser.add_mutually_exclusive_group()

parser.add_argument("-a", "--action", choices=actions, type=str,
                    help=f"Runs the specified script. Available options are " + ", ".join(actions),
                    metavar="")

group.add_argument("-d", "--distro", type=str,
                   help="Specifies which distro is going to be modified." +
                   " (e.g. arch, fedora, debian)", metavar="")

parser.add_argument("-v", "--verbose", action="store_true", help="Print more messages")

group.add_argument("--version", action="version", version="%(prog)s 1.0")

args = parser.parse_args()

if current_platform != "linux":
    raise RuntimeError(f"{current_platform}: platform not supported")
else:
    if __name__ == "__main__":
        if args.verbose:
            print(f"[i] Action set to: {args.action}\n[i] Distribution set to: {args.distro}\n")
            input(f"Press any key to continue.\n")

        try:
            match args.action:
                case "setup-secure-boot":
                    pm = PackageManager()
                    sbm = SecureBootManager()
                    current_user = getuser()
                    package_manager = pm.get_package_manager()

                    if args.verbose:
                        sbm.install_dependencies("preloader-signed", package_manager, verbose=True)
                        sbm.backup_boot_files(verbose=True)
                        sbm.install_shim(current_user, verbose=True)
                    else:
                        sbm.install_dependencies("preloader-signed", package_manager)
                        sbm.backup_boot_files()
                        sbm.install_shim(current_user)

                case "install-tkg-kernel":
                    pm = PackageManager()
                    ki = KernelInstaller()
                    distro = pm.current_distro

                    ki.clone_repo("https://github.com/frogging-family/linux-tkg.git", "linux-tkg")
                    ki.install_kernel("linux-tkg", distro)

                case "install-packages":
                    pm = PackageManager()
                    package_manager = pm.get_package_manager(overridePackageManager=True)

                    if args.verbose:
                        print(f"[i] Package manager to be used: {package_manager}")
                    pm.install_packages(package_manager)

                case "setup-rootfs":
                    raise NotImplementedError("This function is not implemented yet.")

                case "setup-services":
                    pm = PackageManager()
                    sm = ServicesManager()

                    pkglist = pm.get_package_list()
                    services = sm.get_services_list(pkglist)

                    sm.enable_services(services)

                case _:
                    if args.action:
                        raise ValueError(f"{args.action}: invalid action")
                    else:
                        raise ValueError("No action was specified.")
        except Exception:
            raise

