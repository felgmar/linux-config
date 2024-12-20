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

    def install_dependencies(self, verbose: bool = False):
        """
        Installs the necessary packages to setup secure boot.
        """
        pkglist: list[str] = [
            "preloader-signed"
        ]

        pm = PackageManager()
        pm_bin = pm.get_package_manager(override_package_manager=True)

        if verbose:
            print("The package manager has been set to:", pm_bin)

        pm.install_packages(pm_bin, custom_pkglist=pkglist)

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
                        if self.current_user != "root":
                            if verbose:
                                subprocess.run(f"sudo cp -v {file} {file}.backup",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '{file}.backup'")
                                subprocess.run(f"sudo cp '{file}' {file}.backup",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                        else:
                            if verbose:
                                subprocess.run(f"cp -v '{file}' {file}.backup",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '{file}.backup'")
                                subprocess.run(f"cp '{file}' '{file}.backup'",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                    case _:
                        return
            except Exception as e:
                raise e

    def _check_file_access(self, file: str) -> None:
        if not os.access(file, os.R_OK):
            raise FileNotFoundError(file + " is not accessible.")

    def _copy_file(self, file: str, verbose: bool) -> None:
        if self.current_user != "root":
            if file == "/usr/share/preloader-signed/HashTool.efi":
                self._copy_hash_tool(file, verbose)
            elif file == "/usr/share/preloader-signed/PreLoader.efi":
                self._copy_preloader(file, verbose)

    def _copy_hash_tool(self, file: str, verbose: bool) -> None:
        if verbose:
            subprocess.run(f"sudo cp -v '{file}' '/boot/EFI/BOOT'",
                           shell=True, universal_newlines=True,
                           check=True, text=True)
        else:
            print(f"Copying '{file}' to '/boot/EFI/BOOT'")
            subprocess.run(f"sudo cp '{file}' '/boot/EFI/BOOT'",
                           shell=True, universal_newlines=True,
                           check=True, text=True)

    def _copy_preloader(self, file: str, verbose: bool):
        if verbose:
            subprocess.run(f"sudo cp -v '{file}' '/boot/EFI/BOOT'",
                           shell=True, universal_newlines=True,
                           check=True, text=True)
        else:
            print(f"Copying '{file}' to '/boot/EFI/BOOT'")
            subprocess.run(f"sudo cp '{file}' '/boot/EFI/BOOT'",
                           shell=True, universal_newlines=True,
                           check=True, text=True)

    def install_shim(self, verbose: bool = False):
        """
        Installs the shim packages.
        """
        try:
            preloader_files: list[str] = [
                "/usr/share/preloader-signed/HashTool.efi",
                "/usr/share/preloader-signed/PreLoader.efi",
            ]

            for file in preloader_files:
                self._check_file_access(file)
                self._copy_file(file, verbose)
        except Exception as e:
            raise e
