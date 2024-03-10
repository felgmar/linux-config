#!/usr/bin/env python3

from argparse import ArgumentParser
from getpass import getuser
from sys import platform
from modules.kernels.setup import KernelInstaller
from modules.packages.setup import PackageManager
from modules.tools.secure_boot.setup import SecureBootManager

running_os = platform.lower()

actions = [
    "setup-secure-boot", "install-tkg-kernel",
    "setup-rootfs", "setup-packages",
    "setup-services", "install-packages"
]

parser = ArgumentParser(prog="linux-config")
group = parser.add_mutually_exclusive_group()

parser.add_argument("-a", "--action", choices=actions, type=str,
                    help=f"Runs the specified script. Available options are " + ", ".join(actions),
                    metavar="")

group.add_argument("-d", "--distro", type=str, help="Specifies which distro is going to be modified." +
                   " (e.g. arch, fedora, debian)", metavar="")

group.add_argument("-v", "--verbose", action="store_true", help="Print more messages")

group.add_argument("--version", action="version", version="%(prog)s 1.0")

args = parser.parse_args()

if running_os != "linux":
    raise RuntimeError(f"{platform.lower()}: OS not supported")
else:
    if __name__ == "__main__":
        if args.verbose:
            print(f"""
                  action is set to {args.action}
                  distro to be modified is {args.distro}
                  """)

        input(f"[*] {parser.prog} is ready. Press any key to continue.\n")

        try:
            match args.action:
                case "setup-secure-boot":
                    pm = PackageManager()
                    sbm = SecureBootManager()
                    package_manager = pm.get_package_manager(pm.readable_running_distro)

                    if args.verbose:
                        sbm.install_dependencies("preloader-signed", package_manager, verbose=True)
                        sbm.backup_boot_files(verbose=True)
                        sbm.install_shim(getuser(), verbose=True)
                    else:
                        sbm.install_dependencies("preloader-signed", package_manager)
                        sbm.backup_boot_files()
                        sbm.install_shim(getuser())

                case "install-tkg-kernel":
                    pm = PackageManager()
                    ki = KernelInstaller()
                    ki.clone_repo("https://github.com/frogging-family/linux-tkg.git", "linux-tkg")
                    ki.install_kernel("linux-tkg", pm.readable_running_distro)

                case "install-packages":
                    pm = PackageManager()
                    lsb_release_path = pm.readable_lsb_release_path

                    if not lsb_release_path:
                        raise ValueError("Could not find the file lsb_release.")
                    else:
                        if args.verbose:
                            print(f"lsb_release was found at: {lsb_release_path}")

                    pkglist = pm.get_package_list(pm.readable_running_distro)
                    main_pkglist = pm.get_main_packages_list(pm.readable_running_distro)
                    aur_pkglist = pm.get_main_packages_list(pm.readable_running_distro, only_get_aur=True)
                    package_manager = pm.get_package_manager(pm.readable_running_distro, overridePackageManager=True)

                    if args.verbose:
                        print(f"[*] Package manager to be used: {pm.get_package_manager(pm.readable_running_distro)}")

                    pm.install_packages(pkglist, package_manager, getuser())

                case "setup-roofs":
                    raise NotImplementedError("This function is not implemented yet.")

                case "setup-services":
                    raise NotImplementedError("This function is not implemented yet.")

                case _:
                    raise ValueError("[!] unknown action")

        except Exception:
            raise
