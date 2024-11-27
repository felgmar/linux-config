#!/usr/bin/env python3

import getpass
import subprocess
import os

from modules.packages import PackageManager

class SecureBootManager():
    def __init__(self):
        self.current_user: str = getpass.getuser()

    def install_dependencies(self, verbose: bool = False):
        pkglist: list[str] = [
            "preloader-signed"
        ]

        pm = PackageManager()
        pm_bin = pm.get_package_manager(override_package_manager=True)

        if verbose:
            print("The package manager has been set to:", pm_bin)

        pm.install_packages(pm_bin, custom_pkglist=pkglist)

    def backup_boot_files(self, verbose: bool = False) -> None:
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

    def install_shim(self, verbose: bool = False):
        try:
            preloader_files: list[str] = [
                "/usr/share/preloader-signed/HashTool.efi",
                "/usr/share/preloader-signed/PreLoader.efi",
            ]

            for file in preloader_files:
                if not os.access(file, os.R_OK):
                    raise FileNotFoundError(file + " is not accessible.")

                if self.current_user != "root":
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                subprocess.run(f"sudo cp -v '{file}' '/boot/EFI/BOOT'",
                                               shell=True, universal_newlines=True,
                                               check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '/boot/EFI/BOOT'")
                                subprocess.run(f"sudo cp '{file}' '/boot/EFI/BOOT'",
                                               shell=True, universal_newlines=True,
                                               check=True, text=True)
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                subprocess.run(f"sudo cp -v '{file}' '/boot/EFI/BOOT/BOOTX64.EFI'",
                                               shell=True, universal_newlines=True,
                                               check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '/boot/EFI/BOOT/BOOTX64.EFI'")
                                subprocess.run(f"sudo cp '{file}' '/boot/EFI/BOOT/BOOTX64.EFI'",
                                               shell=True, universal_newlines=True,
                                               check=True, text=True)
                        case _:
                            raise ValueError()

                    is_installed: subprocess.CompletedProcess[str] = \
                        subprocess.run("sudo bootctl is-installed", shell=True,
                                       universal_newlines=True, capture_output=True,
                                       check=True, text=True)
                    is_installed_readable: str = str(is_installed).replace("\n", "")

                    if is_installed_readable == "yes":
                        if verbose:
                            print("systemd-boot is already installed")
                            subprocess.run("sudo bootctl update",
                                shell=True, universal_newlines=True, check=True, text=True)
                        else:
                            print("Updating systemd-boot files...")
                            subprocess.run("sudo bootctl update",
                                shell=True, universal_newlines=True, check=True, text=True)
                    elif is_installed_readable == "no":
                        if verbose:
                            print("systemd-boot is not installed")
                            subprocess.run("sudo bootctl install --no-variables",
                                shell=True, universal_newlines=True, check=True, text=True)
                        else:
                            print("Installing systemd-boot bootloader...")
                            subprocess.run("sudo bootctl install --no-variables",
                                            shell=True, universal_newlines=True,
                                            check=True, text=True)
                else:
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                subprocess.run(f"cp -v '{file}' '/boot/EFI/BOOT'",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '/boot/EFI/BOOT'")
                                subprocess.run(f"cp '{file}' '/boot/EFI/BOOT'",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                subprocess.run(f"cp -v '{file}' '/boot/EFI/BOOT/BOOTX64.EFI'",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                            else:
                                print(f"Copying '{file}' to '/boot/EFI/BOOT/BOOTX64.EFI'")
                                subprocess.run(f"cp '{file}' /boot/EFI/BOOT/BOOTX64.EFI",
                                                shell=True, universal_newlines=True,
                                                check=True, text=True)
                        case _:
                            raise ValueError()

                    is_installed = subprocess.run("bootctl is-installed",
                                                  shell=True, universal_newlines=True,
                                                  capture_output=True, check=True, text=True)
                    is_installed_readable: str = str(is_installed).replace("\n", "")

                    if is_installed_readable == "yes":
                        if verbose:
                            print("systemd-boot is installed")
                            subprocess.run("bootctl update",
                                shell=True, universal_newlines=True, check=True, text=True)
                        else:
                            print("Updating systemd-boot files...")
                            subprocess.run("bootctl update",
                                shell=True, universal_newlines=True, check=True, text=True)
                    elif is_installed_readable == "no":
                        if verbose:
                            print("systemd-boot is not installed")
                            subprocess.run("bootctl install --no-variables",
                                shell=True, universal_newlines=True, check=True, text=True)
                        else:
                            print("Installing systemd-boot bootloader...")
                            subprocess.run("bootctl install --no-variables",
                                            shell=True, universal_newlines=True,
                                            check=True, text=True)

            if not self.current_user == "root":
                if not os.path.isfile("/boot/EFI/BOOT/loader.efi"):
                    if verbose:
                        subprocess.run("sudo cp -v '/boot/EFI/systemd/systemd-bootx64.efi'" + \
                                       "'/boot/EFI/BOOT/loader.efi'",
                                       shell=True,universal_newlines=True, check=True, text=True)
                    else:
                        print("Copying file '/boot/EFI/systemd/systemd-bootx64.efi'" + \
                              "to '/boot/EFI/BOOT/loader.efi'...")
                        subprocess.run("sudo cp /boot/EFI/systemd/systemd-bootx64.efi" + \
                                       "'/boot/EFI/BOOT/loader.efi'",
                                        shell=True,universal_newlines=True, check=True, text=True)
            else:
                if not os.path.isfile("/boot/EFI/BOOT/loader.efi"):
                    if verbose:
                        subprocess.run("cp -v '/boot/EFI/systemd/systemd-bootx64.efi'" + \
                                       "'/boot/EFI/BOOT/loader.efi'",
                                        shell=True,universal_newlines=True, check=True, text=True)
                    else:
                        print("Copying file '/boot/EFI/systemd/systemd-bootx64.efi'" + \
                              "to '/boot/EFI/BOOT/loader.efi'...")
                        subprocess.run("cp '/boot/EFI/systemd/systemd-bootx64.efi'" + \
                                       "'/boot/EFI/BOOT/loader.efi'",
                                        shell=True,universal_newlines=True, check=True, text=True)
        except Exception as e:
            raise e
