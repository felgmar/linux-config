#!/usr/bin/env python3

"""
Module containing the SecureBootManager class.
"""

import getpass
import subprocess
import os

from modules.packages import PackageManager

class SecureBootManager():
    """
    Manages secure boot on Linux systems.
    """
    def __init__(self):
        self.current_user: str = getpass.getuser()

    def install_dependencies(self, desktop_environment: str, verbose: bool = False):
        """
        Installs the necessary packages to setup secure boot.
        """
        pkglist: list[str] = [
            "preloader-signed"
        ]

        pm = PackageManager()
        pm_bin = pm.get_package_manager(get_aur_helper=True)

        if verbose:
            print("[VERBOSE] The package manager has been set to:", pm_bin)

        pm.install_packages(pm_bin, desktop_environment, custom_pkglist=pkglist)

    def _check_file_access(self, file: str) -> None:
        if not os.access(file, os.R_OK):
            raise FileNotFoundError(file + " is not accessible.")

    def _copy_file(self, source: str, destination: str, verbose: bool = False):
        command: str | None = None

        if command is None:
            if self.current_user == "root":
                if verbose:
                    command = f"cp -v {source} {destination}"
                else:
                    command = f"cp {source} {destination}"
            else:
                if verbose:
                    command = f"sudo cp -v {source} {destination}"
                else:
                    command = f"sudo cp {source} {destination}"

        try:
            subprocess.run(command, shell=True, universal_newlines=True,
                           check=True, text=True)
        except Exception as e:
            raise e

    def backup_boot_files(self, verbose: bool = False) -> None:
        """
        Backs up the boot files.
        """
        boot_files: list[str] = [
            "/boot/EFI/BOOT/BOOTX64.EFI",
        ]

        for file in boot_files:
            try:
                match file:
                    case "/boot/EFI/BOOT/BOOTX64.EFI":
                        self._check_file_access(file)
                        if verbose:
                            self._copy_file(file, f"{file}.backup", verbose=True)
                        else:
                            self._copy_file(file, f"{file}.backup")
                    case _:
                        raise FileNotFoundError(file)
            except Exception as e:
                raise e

    def install_shim(self, verbose: bool = False):
        """
        Installs the shim packages.
        """
        preloader_files: list[str] = [
            "/usr/share/preloader-signed/HashTool.efi",
            "/usr/share/preloader-signed/PreLoader.efi",
        ]

        systemd_files: list[str] = [
            "/boot/EFI/systemd/systemd-bootx64.efi"
        ]

        for file in preloader_files:
            try:
                match file:
                    case "/usr/share/preloader-signed/HashTool.efi":
                        self._check_file_access(file)
                        self._copy_file(file, "/boot/EFI/BOOT", verbose)
                    case "/usr/share/preloader-signed/PreLoader.efi":
                        self._check_file_access(file)
                        self._copy_file(file, "/boot/EFI/BOOT/BOOTX64.EFI", verbose)
                    case _:
                        self._check_file_access(file)
            except Exception as e:
                raise e

        for file in systemd_files:
            try:
                match file:
                    case "/boot/EFI/systemd/systemd-bootx64.efi":
                        self._check_file_access(file)
                        self._copy_file(file, "/boot/EFI/BOOT/loader.efi", verbose)
                    case _:
                        self._check_file_access(file)
            except Exception as e:
                raise e
