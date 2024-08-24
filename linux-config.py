#!/usr/bin/env python3

import sys, argparse

from modules.kernels import kernel_manager
from modules.packages import package_manager
from modules.secure_boot import secure_boot_manager
from modules.services import services_manager

current_platform = sys.platform.lower()

actions: list[str] = [
    "setup-secure-boot", "install-tkg-kernel",
    "install-packages", "setup-rootfs", "setup-services"
]

parser = argparse.ArgumentParser(prog="linux-config")
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

if __name__ == "__main__":
    if current_platform != "linux":
        raise RuntimeError(f"{current_platform}: platform not supported")

    if args.verbose:
        print(f"[i] Action set to: {args.action}\n[i] Distribution set to: {args.distro}\n")
        input(f"Press any key to continue.\n")

    try:
        match args.action:
            case "setup-secure-boot":
                sbm = secure_boot_manager()
                pm = package_manager()

                if args.verbose:
                    sbm.install_dependencies(verbose=True)
                    sbm.backup_boot_files(verbose=True)
                    sbm.install_shim(verbose=True)
                else:
                    sbm.install_dependencies()
                    sbm.backup_boot_files()
                    sbm.install_shim()

            case "install-tkg-kernel":
                pm = package_manager()
                km = kernel_manager()

                km.repo_url = "https://github.com/frogging-family/linux-tkg.git"
                km.repo_dir = "linux-tkg"

                if args.verbose:
                    km.install_kernel(verbose=True)
                else:
                    km.install_kernel()

            case "install-packages":
                pm = package_manager()
                package_manager = pm.get_package_manager(overridePackageManager=True)

                if args.verbose:
                    print(f"[i] Package manager to be used: {package_manager}")

                pm.install_packages(package_manager)

            case "setup-rootfs":
                raise NotImplementedError("This function is not implemented yet.")

            case "setup-services":
                pm = package_manager()
                sm = services_manager()

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
