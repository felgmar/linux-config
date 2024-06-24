#!/usr/bin/env python3

import getpass, subprocess
from modules.packages.setup import PackageManager

class SecureBootManager():
    def __init__(self):
        self.current_user: str = getpass.getuser()

    def install_dependencies(self, verbose=False):
        pkglist: list[str] = [
            "preloader-signed"
        ]

        pm = PackageManager()
        pm_bin = pm.get_package_manager()

        if pm_bin != "paru" or "yay":
            for pm_override in "yay", "paru":
                if pm_override == "paru" or "yay":
                    package_manager = pm_override

            if verbose:
                if pm_bin != pm_override:
                    print(f"The package manager has been set to: {pm_override}")

        pm.install_packages(package_manager, custom_pkglist=pkglist)

    def backup_boot_files(self, verbose=False) -> None:
        boot_files: list[str] = [
            "/boot/EFI/BOOT/BOOTX64.EFI",
        ]

        for file in boot_files:
            try:
                match file:
                    case "/boot/EFI/BOOT/BOOTX64.EFI":
                        try:
                            if verbose:
                                if self.current_user == "root":
                                    subprocess.run(f"cp -v {file} {file}.backup",
                                        shell=True, universal_newlines=True, text=True)
                                else:
                                    subprocess.run(f"sudo cp -v {file} {file}.backup",
                                        shell=True, universal_newlines=True, text=True)
                            else:
                                if self.current_user == "root":
                                    subprocess.run(f"cp {file} {file}.backup",
                                        shell=True, universal_newlines=True, text=True)
                                else:
                                    subprocess.run(f"sudo cp {file} {file}.backup",
                                        shell=True, universal_newlines=True, text=True)
                        except Exception:
                            raise
            except Exception:
                raise

    def install_shim(self, verbose: bool = False):
        try:
            preloader_files: list[str] = [
                "/usr/share/preloader-signed/HashTool.efi",
                "/usr/share/preloader-signed/PreLoader.efi",
            ]

            if self.current_user != "root":
                for file in preloader_files:
                    #if not access(file, R_OK):
                    #    raise PermissionError(f"The file {file} is not accessible.")
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                subprocess.run(f"sudo cp -v {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                subprocess.run(f"sudo cp {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            continue
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                subprocess.run(f"sudo cp -v {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                subprocess.run(f"sudo cp {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            break

                is_installed: subprocess.CompletedProcess[str] = subprocess.run("sudo bootctl is-installed", shell=True, universal_newlines=True, capture_output=True, text=True)
                is_installed_readable: str = str(is_installed).replace("\n", "")

                if is_installed_readable == "yes":
                    if verbose:
                        print(f"[*] systemd-boot is already installed")
                        subprocess.run("sudo bootctl update",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        subprocess.run("sudo bootctl update",
                            shell=True, universal_newlines=True, text=True)
                elif is_installed_readable == "no":
                    if verbose:
                        print(f"[!] systemd-boot is not installed")
                        subprocess.run("sudo bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        subprocess.run("sudo bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
            else:
                for file in preloader_files:
                    #if not access(file, R_OK) or access(file, W_OK):
                    #    raise PermissionError(f"The file {file} is not accessible.")
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                subprocess.run(f"cp -v {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                subprocess.run(f"cp {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                subprocess.run(f"cp -v {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                subprocess.run(f"cp {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)

                is_installed = subprocess.run("bootctl is-installed",
                                   shell=True, universal_newlines=True,
                                   capture_output=True, text=True)
                is_installed_readable: str = str(is_installed).replace("\n", "")

                if is_installed_readable == "yes":
                    if verbose:
                        print("[*] systemd-boot is installed")
                        subprocess.run("bootctl update",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        subprocess.run("bootctl update",
                            shell=True, universal_newlines=True, text=True)
                elif is_installed_readable == "no":
                    if verbose:
                        print("[!] systemd-boot is not installed")
                        subprocess.run("bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        subprocess.run("bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
        except Exception:
            raise
