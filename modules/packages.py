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
        self.lsb_release_bin: str | None = shutil.which("lsb_release")
        self.PLATFORM: Platform = Platform()
        self.CURRENT_DISTRO: str = self.PLATFORM.get_distro()
        self.CURRENT_USER: str = self.PLATFORM.get_user()

        if not self.lsb_release_bin:
            raise FileNotFoundError("lsb_release: not found")

    def get_package_manager(self, verbose: bool = False) -> str:
        """
        Returns the package manager based on the current distribution.
        """
        pm_bin: str | None = None

        package_managers = [
            "apt",
            "dnf",
            "pacman",
            "zypper"
        ]

        aur_helpers = [
            "paru",
            "yay"
        ]

        for helper in aur_helpers + package_managers:
            if not shutil.which(helper) and verbose:
                print(helper, "was not found")
            pm_bin = helper
            break

        if pm_bin is None:
            raise ValueError("No package manager could be set.")

        return pm_bin

    def install_aur_helper(self, distro: str, package_manager: str):
        """
        Installs an AUR helper based on the distribution.
        """
        match distro:
            case "arch":
                match package_manager:
                    case "paru":
                        raise NotImplementedError()
                    case "yay":
                        raise NotImplementedError()
                    case _:
                        raise ValueError(package_manager, "invalid package manager")
            case _:
                raise ValueError(distro, ": unsupported distribution")

    def convert_list_to_str(self, list_to_convert: list[str]) -> str:
        """
        Converts a list to a string.
        """
        new_list = ' '.join(list_to_convert)

        return new_list

    def get_main_packages_list(self) -> list[str]:
        """
        Returns a list of main packages based on the current distribution.
        """
        match self.CURRENT_DISTRO:
            case "arch":
                with open("config/arch/packages/main.txt", "r", encoding="utf-8") as file:
                    MAIN_PACKAGE_LIST = file.read().splitlines()
                return MAIN_PACKAGE_LIST
            case _:
                raise ValueError(self.CURRENT_DISTRO, "is not supported.")

    def get_desktop_environment(self) -> str:
        """
        Returns the desktop environment based on the user's choice.
        """
        desktop_environment = input("Choose a desktop environment [gnome/kde/xfce]: ")

        if not desktop_environment:
            raise ValueError("No desktop environment was specified.")

        match desktop_environment:
            case "gnome":
                return "gnome"
            case "kde" | "plasma":
                return "kde"
            case "xfce":
                return "xfce"
            case _:
                raise ValueError(f"{desktop_environment}: invalid or unrecognized desktop environment")

    def get_package_list(self, desktop_environment: str, only_get_aur: bool = False) -> list[str]:
        """
        Returns a list of packages based on the desktop environment.
        """
        match self.CURRENT_DISTRO:
            case "arch":
                aur = [
                    "archlinux-artwork",
                    "github-desktop-bin",
                    "lib32-mangohud-git",
                    "mangohud-git",
                    "mkinitcpio-firmware",
                    "plymouth-theme-archlinux",
                    "preloader-signed",
                    "rate-mirrors",
                    "ventoy-bin",
                    "visual-studio-code-bin",
                ]

                gnome = [
                    "gdm",
                    "gnome-backgrounds",
                    "gnome-browser-connector",
                    "gnome-control-center",
                    "gnome-disk-utility",
                    "gnome-keyring",
                    "gnome-themes-extra",
                    "gvfs",
                    "gvfs-mtp",
                    "gvfs-nfs",
                    "gvfs-google",
                    "libappindicator-gtk3",
                    "malcontent",
                    "nautilus"
                ]

                kde = [
                    "bluedevil",
                    "breeze-gtk",
                    "dolphin",
                    "gnome-keyring",
                    "kde-gtk-config",
                    "kdialog",
                    "kscreen",
                    "kwalletmanager",
                    "kwallet-pam",
                    "plasma-desktop",
                    "plasma-nm",
                    "plasma-pa",
                    "powerdevil",
                    "sddm"
                ]

                xfce = [
                    "xfce4"
                ]
            case _:
                raise ValueError(self.CURRENT_DISTRO, "unsupported distro")

        if only_get_aur and self.CURRENT_DISTRO == "arch":
            return aur

        match desktop_environment:
            case "gnome":
                return gnome
            case "kde" | "plasma" | "kdeplasma":
                return kde
            case "xfce":
                return xfce
            case _:
                raise ValueError(desktop_environment, "invalid desktop environment")

    def install_packages(self, package_manager: str,
                         desktop_environment: str,
                         custom_pkglist: list[str] | None) -> None:
        """
        Installs packages based on the current distribution.
        """
        packages: str | None = None
        command: list[str] = []

        if not custom_pkglist is None:
            packages = self.convert_list_to_str(custom_pkglist)
        else:
            main_packages = self.get_main_packages_list()
            main_pkglist = self.convert_list_to_str(main_packages)

            extra_packages = self.get_package_list(desktop_environment)
            extra_pkglist = self.convert_list_to_str(extra_packages)

            match self.CURRENT_DISTRO:
                case "arch":
                    aur_packages = self.get_package_list(desktop_environment,
                                                         only_get_aur=True)
                    aur_pkglist = self.convert_list_to_str(aur_packages)
                    packages = main_pkglist + " " + extra_pkglist + " " + aur_pkglist
                case _:
                    packages = main_pkglist + " " + extra_pkglist + " "

        if self.CURRENT_USER == "root":
            

            match package_manager:
                case "apt":
                    command.extend([
                        package_manager,
                        "update",
                        "&&",
                        package_manager,
                        "install",
                        packages
                    ])
                case "pacman":
                    command.extend([
                        package_manager,
                        "-Syu",
                        "--needed",
                        "&&",
                        package_manager,
                        "-S",
                        packages
                    ])
                case "dnf":
                    cmd = f"{package_manager} update &&" \
                          f"{package_manager} install {packages}"
                case "paru" | "yay":
                    raise PermissionError("{0} is an AUR helper and it cannot be ran as {1}"
                                          .format(package_manager, self.CURRENT_USER))
                case _:
                    raise NotImplementedError(package_manager, "unknown package manager.")
        else:
            match package_manager:
                case "apt":
                    cmd = f"sudo {package_manager} update &&" + \
                          f"sudo {package_manager} install {packages}"
                case "pacman":
                    cmd = f"sudo {package_manager} -Syu --needed {packages}"
                case "dnf":
                    cmd = f"sudo {package_manager} update &&" \
                          f"sudo {package_manager} install {packages}"
                case "paru" | "yay":
                    if custom_pkglist:
                        cmd = f"{package_manager} -S --needed --sudoloop {packages}"
                    else:
                        cmd = f"{package_manager} -Syu --needed --sudoloop {packages}"
                case _:
                    raise NotImplementedError(package_manager, "unknown package manager.")

        try:
            subprocess.run(cmd, shell=True, universal_newlines=True, check=True, text=True)
        except Exception as e:
            raise e
